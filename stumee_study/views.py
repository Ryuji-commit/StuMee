from django.views.generic.edit import ModelFormMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from .models import Course, Category
from .forms import CreateCourseForm, CreateCategoryForm, UpdateCourseForm, CourseCertificationForm


# Course list
@login_required(redirect_field_name=None)
def study_index(request):
    course_list = Course.objects.order_by('-make_date')
    category_list = Category.objects.all()

    if request.method == 'POST':
        form = CreateCategoryForm(request.POST)
        if form.is_valid():
            if request.user.user_auth == 2:
                form.save()
    else:
        form = CreateCategoryForm()

    if request.method == 'GET':
        course_certification_form = CourseCertificationForm(request.GET)
        course_id = request.GET.get('course_id')
        if course_certification_form.is_valid():
            course = Course.objects.get(id=course_id)
            input_key = course_certification_form.cleaned_data['certification_password_course']
            if course.certification_key == input_key:
                course.students.add(request.user)
                course.save()
                messages.success(request, f'{course.title}への認証に成功しました!')
                return redirect(reverse('stumee_chat:chat_question', args=[course_id, request.user.id]))
            else:
                messages.error(request, f'{course.title}への認証に失敗しました', extra_tags='danger')
                return redirect(reverse('stumee_study:study_index'))
    else:
        course_certification_form = CourseCertificationForm()

    return render(
        request,
        'stumee_study/study_index.html',
        {
            'course_list': course_list,
            'category_list': category_list,
            'form': form,
            'course_certification_form': course_certification_form,
        }
    )


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
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('stumee_study:study_index')


class DeleteCourseView(LoginRequiredMixin, generic.DeleteView):
    model = Course

    def get_success_url(self):
        return reverse('stumee_study:study_index')

    def delete(self, request, *args, **kwargs):
        self.object = course = self.get_object()
        if request.user == course.create_user:
            course.delete()

        return redirect(self.get_success_url())


class UpdateCourseView(LoginRequiredMixin, generic.UpdateView):
    model = Course
    template_name = 'stumee_study/update_course.html'
    form_class = UpdateCourseForm

    def get_success_url(self):
        return reverse('stumee_study:study_index')

    def form_valid(self, form):
        course = form.save(commit=False)
        if self.request.user == course.create_user:
            course.save()
            form.save_m2m()

        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(UpdateCourseView, self).get_context_data(**kwargs)
        context['updated_course'] = Course.objects.filter(id=self.kwargs['pk']).first()
        return context







