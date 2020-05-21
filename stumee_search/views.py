from django.views import generic
from django.db.models import Q

from stumee_meeting.models import Thread


# The ListView for search function of Meeting
class MeetingSearchView(generic.ListView):
    template_name = 'stumee_search/search_result.html'
    context_object_name = 'search_results'

    def get_queryset(self):
        search_word = self.request.GET.get('meeting_search_form')
        if search_word:
            return Thread.objects.filter(
                Q(title__icontains=search_word) | Q(tag__name__icontains=search_word)
            ).order_by('-is_picked', '-good_count', '-make_date').distinct()
        else:
            return Thread.objects.order_by('-is_picked', '-good_count', '-make_date')

    def get_context_data(self, **kwargs):
        context = super(MeetingSearchView, self).get_context_data(**kwargs)
        search_word = self.request.GET.get('meeting_search_form')
        context['search_word'] = search_word
        return context
