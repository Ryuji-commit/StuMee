from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser
from stumee_meeting.models import Thread, Comment
from . import forms


# Create your views here.
def home(request):
    return render(
        request,
        'stumee_auth/home.html',
    )


@login_required
def user_setting(request):
    initial_dict = {
        'username': request.user.username,
        'user_auth': request.user.user_auth,
    }
    user = request.user
    if request.method == "POST":
        form = forms.ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
        else:
            return redirect('stumee_meeting:index')
    else:
        form = forms.ProfileForm(initial=initial_dict)
    return render(
        request,
        'stumee_auth/user_setting.html',
        {
            'form': form,
            'user': user,
        }
    )


# User Profile Page
class UserProfileView(LoginRequiredMixin, generic.DetailView):
    model = CustomUser
    template_name = 'stumee_auth/user_profile.html'
    context_object_name = 'user_profile'

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        user_id = self.kwargs['pk']
        user = CustomUser.objects.get(id=user_id)
        context['user_comments'] = Comment.objects.filter(user=user)
        return context


