from django.urls import path

from . import views

app_name = 'stumee_search'
urlpatterns = [
    path('', views.MeetingSearchView.as_view(), name='meeting_search'),
]