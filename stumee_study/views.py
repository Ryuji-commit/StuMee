from django.views.generic.edit import ModelFormMixin
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from .models import Course, Category
from .forms import CreateCourseForm, CreateCategoryForm


# Course list
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
    return render(
        request,
        'stumee_study/study_index.html',
        {
            'course_list': course_list,
            'category_list': category_list,
            'form': form,
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
            course.save_m2m()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('stumee_study:study_index')



