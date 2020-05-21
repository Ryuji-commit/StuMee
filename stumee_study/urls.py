from django.urls import path

from . import views

app_name = 'stumee_study'
urlpatterns = [
    path('', views.temp_view, name='temp_view'),
]
