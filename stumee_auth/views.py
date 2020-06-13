from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import CustomUser, CertificationPass
from stumee_meeting.models import Thread, Comment
from . import forms


# Create your views here.
def home(request):
    return render(
        request,
        'stumee_auth/home.html',
    )


# The view for setting user profile
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


class CustomCertificationView(generic.FormView):
    template_name = 'stumee_auth/login.html'
    form_class = forms.CertificationForm
    success_url = reverse_lazy('social:begin', args=['google-oauth2'])

    def form_valid(self, form):
        certification_pass = form.cleaned_data['certification_login_password']
        if CertificationPass.objects.filter(login_certification_key=certification_pass).exists():
            return super(CustomCertificationView, self).form_valid(form)
        else:
            redirect_url = reverse('stumee_auth:home')
            return redirect(redirect_url)


