from django.urls import path

from . import views

app_name = 'stumee_chat'
urlpatterns = [
    path('<int:course_id>/question/<int:user_id>/', views.chat_question, name='chat_question'),
    path('<int:course_id>/discussion/', views.chat_discussion, name='chat_discussion'),
    path('response_unread_question/', views.response_for_unread_question, name='polling-for-unread-question'),
]
