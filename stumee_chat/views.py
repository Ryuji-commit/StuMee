from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def chat_question(request, course_id):
    return render(request, 'stumee_chat/chat_question.html', {
        'course_id': course_id,
    })
