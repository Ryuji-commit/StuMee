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
        profile_form = forms.ProfileForm(request.POST, request.FILES, instance=request.user)
        change_authority_ta_form = forms.ChangeAuthorityToTA(request.POST)
        change_authority_teacher_form = forms.ChangeAuthorityToTeacher(request.POST)

        # TAへの権限変更認証キーが入力されたら
        if change_authority_ta_form.is_valid():
            input_key = change_authority_ta_form.cleaned_data['certification_password_change_auth_TA']
            if CertificationPass.objects.filter(change_ta_certification_key=input_key).exists():
                initial_dict['user_auth'] = 1
                profile_form = forms.ProfileForm(initial=initial_dict)
            else:
                redirect_url = reverse('stumee_auth:home')
                return redirect(redirect_url)

        # Teacherへの権限変更認証キーが入力されたら
        if change_authority_teacher_form.is_valid():
            input_key = change_authority_teacher_form.cleaned_data['certification_password_change_auth_Teacher']
            if CertificationPass.objects.filter(change_teacher_certification_key=input_key).exists():
                initial_dict['user_auth'] = 2
                profile_form = forms.ProfileForm(initial=initial_dict)
            else:
                redirect_url = reverse('stumee_auth:home')
                return redirect(redirect_url)

        # プロフィールは無条件に変更できる。(認証キーではじかれたらリダイレクトするはずなので)
        # Warning! : ここら辺の処理は見直しやテストが必要です。
        if profile_form.is_valid():
            profile_form.save()

    else:
        profile_form = forms.ProfileForm(initial=initial_dict)
        change_authority_ta_form = forms.ChangeAuthorityToTA()
        change_authority_teacher_form = forms.ChangeAuthorityToTeacher()

    return render(
        request,
        'stumee_auth/user_setting.html',
        {
            'form': profile_form,
            'change_ta_form': change_authority_ta_form,
            'change_teacher_form': change_authority_teacher_form,
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


# もしis_certificatedがTrueならホームに、Falseならフォームを入力
class CustomCertificationView(generic.FormView):
    template_name = 'stumee_auth/login.html'
    form_class = forms.LoginCertificationForm
    success_url = reverse_lazy('stumee_auth:home')

    def get(self, request, *args, **kwargs):
        # もし認証済みであれば入力の必要がないためホームにリダイレクト
        if request.user.is_certificated:
            redirect_url = reverse_lazy('stumee_auth:home')
            return redirect(redirect_url)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        certification_pass = form.cleaned_data['certification_password_login']
        # 入力した認証キーがあっていればホームにリダイレクト
        if CertificationPass.objects.filter(login_certification_key=certification_pass).exists():
            request_user = self.request.user
            request_user.is_certificated = True
            request_user.save()
            return super(CustomCertificationView, self).form_valid(form)
        else:
            # 間違っていればログアウトさせる
            redirect_url = reverse_lazy('stumee_auth:logout')
            return redirect(redirect_url)


