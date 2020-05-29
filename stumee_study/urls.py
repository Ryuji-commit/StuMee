from django.urls import path

from . import views

app_name = 'stumee_study'
urlpatterns = [
    path('', views.study_index, name='study_index'),
    path('create_course', views.CreateCourseView.as_view(), name='create_course'),
    path('delete_course/<int:pk>', views.DeleteCourseView.as_view(), name='delete_course'),
]
