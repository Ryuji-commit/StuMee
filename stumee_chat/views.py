from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from django import forms
from django.urls import reverse_lazy
from django.utils.html import strip_tags
import json
import time
import datetime

from .models import Message, Channel
from stumee_study.models import Course
from stumee_auth.models import CustomUser
from .forms import FileUploadForm, ProblemNumsUploadForm

# Create your views here.
@login_required(redirect_field_name=None)
def chat_question(request, course_id, user_id):
    course = Course.objects.get(id=course_id)
    user = CustomUser.objects.get(id=user_id)
    channel, bool = Channel.objects.get_or_create(
        course=course,
        user=user,
        is_discussion=False,
    )

    student_channel = Channel.objects.exclude(user=course.create_user).filter(course=course).order_by('user__username')
    chat_messages = Message.objects.filter(channel__id=channel.id).order_by('created_at')

    # 授業時間が設定されていれば、授業時間外であることを通知
    if course.class_start_time and course.class_end_time:
        time_now = datetime.datetime.now().time()
        if not course.class_start_time <= time_now <= course.class_end_time:
            messages.info(request, f'授業時間外です')

    if request.method == 'GET':
        problem_nums_form = ProblemNumsUploadForm()
        if course.problem_nums:
            problem_nums = course.problem_nums
            choices = [(i+1, "問題{}".format(i+1)) for i in range(problem_nums)]
            choices.append((problem_nums+1, "終了"))
            problem_nums_form.fields['problem_being_solved'].choices = choices
            problem_nums_form.fields['problem_being_solved'].initial =\
                channel.problem_being_solved if channel.problem_being_solved else 1
        else:
            problem_nums_form.fields['problem_being_solved'].widget = forms.HiddenInput()
            problem_nums_form.fields['problem_being_solved'].choices = [(-1, "入力の必要はありません")]

    return render(request, 'stumee_chat/chat_question.html', {
        'course_id': course_id,
        'user_id': user_id,
        'chat_messages': chat_messages,
        'student_channel': student_channel,
        'form': FileUploadForm(),
        'problem_nums_form': problem_nums_form,
        'class_start_time': course.class_start_time,
        'class_end_time': course.class_end_time,
        'this_channel': channel,
    })


@login_required(redirect_field_name=None)
def chat_discussion(request, course_id):
    course = Course.objects.get(id=course_id)
    # もし不正アクセスがあればindexページにリダイレクト
    if not CustomUser.objects.filter(
            Q(staffs=course) | Q(create_user=course), Q(id=request.user.id)
    ).exists():
        return redirect('stumee_study:study_index')

    user = course.create_user
    channel, bool = Channel.objects.get_or_create(
        course=course,
        user=user,
        is_discussion=True,
    )

    # 授業時間が設定されていれば、授業時間外であることを通知
    if course.class_start_time and course.class_end_time:
        time_now = datetime.datetime.now().time()
        if not course.class_start_time <= time_now <= course.class_end_time:
            messages.info(request, f'授業時間外です')

    session_shared_message = request.session.pop('shared_message', '')

    student_channel = Channel.objects.exclude(user=user).filter(course=course).order_by('user__username')
    chat_messages = Message.objects.filter(channel__id=channel.id).order_by('created_at')
    return render(request, 'stumee_chat/chat_discussion.html', {
        'course_id': course_id,
        'chat_messages': chat_messages,
        'student_channel': student_channel,
        'form': FileUploadForm(),
        'class_start_time': course.class_start_time,
        'class_end_time': course.class_end_time,
        'session_shared_message': session_shared_message,
    })


def response_for_unread_question(request, course_id):
    previous_data = json.loads(request.body)
    course = Course.objects.get(id=course_id)
    max_seconds_of_connection = 20

    for _ in range(max_seconds_of_connection):
        student_channel = Channel.objects.exclude(user=course.create_user).filter(course=course, is_active=True)
        students_list = []

        for channel in student_channel:
            student_dict = {"id": channel.user.id, "username": channel.user.username}
            students_list.append(student_dict)

        if sorted(students_list, key=lambda x: x["id"]) != sorted(previous_data, key=lambda x: x["id"]):
            response = json.dumps(students_list)
            return JsonResponse(response, safe=False)
        else:
            time.sleep(1)

    response = json.dumps(students_list)
    return JsonResponse(response, safe=False)


def process_for_uploaded_file(request):
    form = FileUploadForm(files=request.FILES)
    if form.is_valid():
        url = form.save()
        file_obj = request.FILES['file']
        return JsonResponse({'url': url, 'filename': file_obj.name})
    return HttpResponseBadRequest()


def inactivate_channel(request, course_id, user_id):
    course = Course.objects.get(id=course_id)
    student = CustomUser.objects.get(id=user_id)
    channel = Channel.objects.get(course=course, user=student)
    if channel.is_active:
        message = "processed accordingly"
        channel.is_active = False
        channel.save()
    else:
        message = "failed inactivate"
    return JsonResponse(data={'message': message})


def receive_and_save_problem_nums(request):
    received_data = json.loads(request.body)
    course_id = received_data['course_id']
    user_id = received_data['user_id']
    problem_nums = received_data['problem_nums']

    course = Course.objects.get(id=course_id)
    student = CustomUser.objects.get(id=user_id)
    channel = Channel.objects.get(course=course, user=student)

    channel.problem_being_solved = problem_nums
    channel.save()
    return JsonResponse(data={'problem_nums': problem_nums})


def student_info_of_the_course(request, course_id):
    course = Course.objects.get(id=course_id)
    # もし不正アクセスがあればindexページにリダイレクト
    if not CustomUser.objects.filter(
            Q(staffs=course) | Q(create_user=course), id=request.user.id
    ).exists():
        return redirect('stumee_study:study_index')
    students_number = course.students.count()
    students_message_number = Message.objects.filter(channel__course=course, channel__is_discussion=False).count()

    questioners = Message.objects.filter(
        channel__course=course, channel__is_discussion=False, channel__user=F('user')
    ).order_by('channel__pk').distinct('channel__pk')
    questioners_number = questioners.count()
    today_questioners_number = questioners.filter(created_at__date=datetime.date.today()).count()

    return render(request, 'stumee_chat/student-info-of-the-course.html', {
        'course': course,
        'students_number': students_number,
        'students_message_number': students_message_number,
        'questioners_number': questioners_number,
        'today_questioners_number': today_questioners_number,
    })


def response_students_progress_data(request):
    course_id = request.POST.get('course_id')
    course = Course.objects.get(id=course_id)
    labels = ["問題 {}".format(i+1) for i in range(course.problem_nums)]
    labels.append("終了")

    students_progress_data = []
    students_channels = Channel.objects.filter(course=course, is_discussion=False)
    for problem_number in range(course.problem_nums+1):
        students_progress_data.append(students_channels.filter(problem_being_solved=problem_number+1).count())
    data_sets = [{
        "label": "学生の進捗状況(5分毎更新)",
        "data": students_progress_data
    }]
    response_dict = {
        "labels": labels,
        "datasets": data_sets,
        "options": {}
    }
    return JsonResponse(response_dict)


def response_list_of_past_messages(request):
    received_data = json.loads(request.body)
    course_id = received_data['course_id']
    is_self_messages = received_data['is_self_messages']
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return JsonResponse(data={}, status=404)

    if is_self_messages:
        # 自分のメッセージをセット
        response_messages = Message.objects.exclude(channel__user=course.create_user).filter(
            channel__course=course, channel__is_discussion=False, user=request.user
        ).order_by('-created_at')[:15]
    else:
        # 学生のメッセージをセット
        response_messages = Message.objects.exclude(channel__user=course.create_user).filter(
            channel__course=course, channel__user=F('user')
        ).order_by('-created_at')[:15]

    response_data = []
    for message in response_messages:
        message_user_id = message.channel.user.id
        message_username = message.channel.user.username
        message_content = strip_tags(message.content)
        if len(message_content) >= 20:
            message_content = message_content[:20]

        response_data.append({'course_id': course_id,
                              'user_id': message_user_id,
                              'content': message_content,
                              'user_name': message_username})

    return JsonResponse(json.dumps(response_data), safe=False)


def save_shared_message_to_session(request):
    received_data = json.loads(request.body, strict=False)
    course_id = received_data['course_id']
    shared_message = received_data['shared_message']
    request.session['shared_message'] = shared_message

    response_message = "セッションへの保存に失敗しました"
    if 'shared_message' in request.session:
        response_message = "正常に保存されました"
    redirect_url = reverse_lazy('stumee_chat:chat_discussion', kwargs={'course_id': course_id})
    return JsonResponse({'redirect_url': redirect_url, 'response_message': response_message})
