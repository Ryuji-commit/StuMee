from django import template

from stumee_study.models import Course
from stumee_auth.models import CustomUser

# Djangoのテンプレートタグライブラリ
register = template.Library()

# staffかどうか判別
@register.filter
def judge_if_staffs(course_id):
    course = Course.objects.get(id=course_id)
    return list(CustomUser.objects.filter(staffs=course).values_list('id', flat=True))
