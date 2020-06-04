from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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
    )
    messages = Message.objects.filter(channel__id=channel.id).order_by('created_at')
    return render(request, 'stumee_chat/chat_question.html', {
        'course_id': course_id,
        'user_id': user_id,
        'messages': messages,
    })
