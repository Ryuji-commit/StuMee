from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse, HttpResponseBadRequest
from django import forms
import json
import time

from .models import Message, Channel
from stumee_study.models import Course
from stumee_auth.models import CustomUser
from .forms import FileUploadForm, ProblemNumsUploadForm

# Create your views here.
@login_required
def chat_question(request, course_id, user_id):
    course = Course.objects.get(id=course_id)
    user = CustomUser.objects.get(id=user_id)
    channel, bool = Channel.objects.get_or_create(
        course=course,
        user=user,
        is_discussion=False,
    )

    student_channel = Channel.objects.exclude(user=course.create_user).filter(course=course).order_by('user__username')
    messages = Message.objects.filter(channel__id=channel.id).order_by('created_at')

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
        'chat_messages': messages,
        'student_channel': student_channel,
        'form': FileUploadForm(),
        'problem_nums_form': problem_nums_form,
    })


@login_required
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

    student_channel = Channel.objects.exclude(user=user).filter(course=course).order_by('user__username')
    messages = Message.objects.filter(channel__id=channel.id).order_by('created_at')
    return render(request, 'stumee_chat/chat_discussion.html', {
        'course_id': course_id,
        'chat_messages': messages,
        'student_channel': student_channel,
        'form': FileUploadForm(),
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
    return render(request, 'stumee_chat/student-info-of-the-course.html', {
        'course': course,
        'students_number': students_number,
        'students_message_number': students_message_number,
    })


def response_students_progress_data(request):
    course_id = request.POST.get('course_id')
    course = Course.objects.get(id=course_id)
    labels = ["問題 {}".format(i+1) for i in range(course.problem_nums)]
    labels.append("終了")

    data = []
    students_channels = Channel.objects.filter(course=course, is_discussion=False)
    for problem_number in range(course.problem_nums+1):
        data.append(students_channels.filter(problem_being_solved=problem_number+1).count())
    data_sets = [{
        "label": "学生の進捗状況(5分毎更新)",
        "data": data
    }]
    response_dict = {
        "labels": labels,
        "datasets": data_sets,
        "options": {}
    }
    return JsonResponse(response_dict)
