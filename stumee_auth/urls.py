from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = 'stumee_auth'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.CustomCertificationView.as_view(), name='certification-page'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('setting/', views.user_setting, name='user_profile'),
    path('<int:pk>/profile/', views.UserProfileView.as_view(), name='profile'),
]
