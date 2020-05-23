from django.urls import path

from . import views

app_name = 'stumee_study'
urlpatterns = [
    path('', views.StudyIndexView.as_view(), name='study_index'),
    path('create_course', views.CreateCourseView.as_view(), name='create_course'),
]
