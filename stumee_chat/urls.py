from django.urls import path

from . import views

app_name = 'stumee_chat'
urlpatterns = [
    path('<int:course_id>/question/<int:user_id>/', views.chat_question, name='chat_question'),
]
