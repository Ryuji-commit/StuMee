from django.urls import path

from . import views

app_name = 'stumee_search'
urlpatterns = [
    path('meeting/', views.MeetingSearchView.as_view(), name='meeting_search'),
    path('study/', views.StudySearchView.as_view(), name='study_search'),
]
