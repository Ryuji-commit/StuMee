from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Message, Channel
from stumee_study.models import Course
from stumee_auth.models import CustomUser

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

    student_channel = Channel.objects.exclude(user=course.create_user).filter(course=course).order_by('is_active')
    messages = Message.objects.filter(channel__id=channel.id).order_by('created_at')
    return render(request, 'stumee_chat/chat_question.html', {
        'course_id': course_id,
        'user_id': user_id,
        'messages': messages,
        'student_channel': student_channel,
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

    student_channel = Channel.objects.exclude(user=user).filter(course=course)
    messages = Message.objects.filter(channel__id=channel.id).order_by('created_at')
    return render(request, 'stumee_chat/chat_discussion.html', {
        'course_id': course_id,
        'messages': messages,
        'student_channel': student_channel,
    })
