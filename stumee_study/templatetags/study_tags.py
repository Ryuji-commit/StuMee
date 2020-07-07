from django import template
from django.db.models import Q

from stumee_study.models import Course
from stumee_auth.models import CustomUser


# Djangoのテンプレートタグライブラリ
register = template.Library()

# staffのユーザidリストを返却
@register.filter
def judge_if_staffs(course_id):
    course = Course.objects.get(id=course_id)
    return list(CustomUser.objects.filter(
        Q(staffs=course) | Q(create_user=course)
    ).distinct().values_list('id', flat=True))


# studentのユーザidリストを返却
@register.filter
def judge_if_students(course_id):
    course = Course.objects.get(id=course_id)
    return list(CustomUser.objects.filter(students=course).values_list('id', flat=True))
