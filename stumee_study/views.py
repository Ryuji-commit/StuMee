from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from .models import Course
from .forms import CreateCourseForm


# Course list
class StudyIndexView(generic.ListView):
    model = Course
    template_name = 'stumee_study/study_index.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        return Course.objects.order_by('-make_date')


# Make Course
class CreateCourseView(LoginRequiredMixin, generic.CreateView):
    model = Course
    template_name = 'stumee_study/create_course.html'
    form_class = CreateCourseForm

    def form_valid(self, form):
        course = form.save(commit=False)
        user = self.request.user
        course.create_user = user
        if user.user_auth == 2:
            course.save()
            course.save_m2m()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('stumee_study:study_index')

