from django.views import generic
from django.db.models import Q

from stumee_meeting.models import Thread
from stumee_study.models import Course, Category


# The ListView for search function of Meeting
class MeetingSearchView(generic.ListView):
    template_name = 'stumee_search/meeting_search_result.html'
    context_object_name = 'threads_list'

    def get_queryset(self):
        search_word = self.request.GET.get('meeting_search_form')
        if search_word:
            return Thread.objects.filter(
                Q(title__icontains=search_word) |
                Q(tag__name__icontains=search_word) |
                Q(description__icontains=search_word)
            ).order_by('-is_picked', '-good_count', '-make_date').distinct()
        else:
            return Thread.objects.order_by('-is_picked', '-good_count', '-make_date')

    def get_context_data(self, **kwargs):
        context = super(MeetingSearchView, self).get_context_data(**kwargs)
        search_word = self.request.GET.get('meeting_search_form')
        context['search_word'] = search_word
        return context


# The ListView for search function of Study
class StudySearchView(generic.ListView):
    template_name = 'stumee_search/study_search_result.html'
    context_object_name = 'search_results'

    def get_queryset(self):
        search_word = self.request.GET.get('study_search_form')
        if search_word:
            return Course.objects.filter(
                Q(title__icontains=search_word) |
                Q(category__name__icontains=search_word) |
                Q(create_user__username__icontains=search_word)
            ).order_by('-make_date').distinct()
        else:
            return Course.objects.order_by('-make_date')

    def get_context_data(self, **kwargs):
        context = super(StudySearchView, self).get_context_data(**kwargs)
        search_word = self.request.GET.get('study_search_form')
        context['search_word'] = search_word
        context['category_list'] = Category.objects.all()
        return context
