from django.urls import path

from . import views

app_name = 'stumee_chat'
urlpatterns = [
    path('<int:course_id>/question/<int:user_id>/', views.chat_question, name='chat_question'),
    path('<int:course_id>/discussion/', views.chat_discussion, name='chat_discussion'),
    path('<int:course_id>/response_unread_/', views.response_for_unread_question, name='polling-for-unread-question'),
    path('process_for_uploaded_file/', views.process_for_uploaded_file, name='process_for_uploaded_file'),
    path('<int:course_id>/inactivate_channel/<int:user_id>/', views.inactivate_channel, name='inactivate-channel'),
    path('receive_and_save_problem_nums', views.receive_and_save_problem_nums, name='post-problem-nums'),
    path('<int:course_id>/students_info_of_this_course/', views.student_info_of_the_course, name='students-info'),
    path('students_progress_data/', views.response_students_progress_data, name='students-progress-data'),
    path('save_shared_message/', views.save_shared_message_to_session, name='save-shared-message')
]
