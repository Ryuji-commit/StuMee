from django.shortcuts import get_object_or_404, render, redirect
from django.http.response import JsonResponse
from django.views import generic
from taggit.models import Tag
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .models import Thread, Comment, ThreadGood, CommentGood
from stumee_auth.models import CustomUser
from . import forms
# Create your views here.


# Threads list
class IndexView(generic.ListView):
    template_name = 'stumee_meeting/index.html'
    context_object_name = 'latest_threads_list'

    def get_queryset(self):
        return Thread.objects.order_by('-is_picked', '-good_count', '-make_date')


# Ask question
@login_required
def post_thread(request):
    if request.method == "POST":
        form = forms.ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.user = request.user
            thread.save()
            form.save_m2m()
            return redirect('stumee_meeting:index')
    else:
        form = forms.ThreadForm()
    return render(
        request,
        'stumee_meeting/post_thread.html',
        {
            'form': form,
        }
    )


# Thread detail
@login_required
def thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    comments = Comment.objects.filter(thread=thread).order_by('-good_count')
    thread.good_count = ThreadGood.objects.filter(thread=thread).count()
    thread.save()
    for thread_comment in thread.comment_set.all():
        thread_comment.good_count = CommentGood.objects.filter(comment=thread_comment).count()
        thread_comment.save()

    if request.method == "POST":
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.no = Comment.objects.filter(thread=thread).count()+1
            comment.user = request.user
            comment.thread = thread
            comment.save()
    else:
        form = forms.CommentForm()
    return render(
        request,
        'stumee_meeting/thread.html',
        {
            'thread': thread,
            'form': form,
            'comments': comments,
        }
    )


# Add good for thread
@login_required
def add_good_for_thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    good_user_list = [thread_good.user.id for thread_good in ThreadGood.objects.filter(thread=thread).all()]
    if request.method == "POST":
        if request.user.id in good_user_list:
            ThreadGood.objects.filter(user=request.user, thread=thread).delete()
        else:
            thread_good = ThreadGood.objects.create(user=request.user, thread=thread)
            thread_good.save()
        d = {
            'count': ThreadGood.objects.filter(thread=thread).count(),
        }
        return JsonResponse(d)


# Add good for comment
@login_required
def add_good_for_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    good_user_list = [comment_good.user.id for comment_good in CommentGood.objects.filter(comment=comment).all()]
    if request.method == "POST":
        if request.user.id in good_user_list:
            CommentGood.objects.filter(user=request.user, comment=comment).delete()
        else:
            comment_good = CommentGood.objects.create(user=request.user, comment=comment)
            comment_good.save()
        d = {
            "id": comment_id,
            "count": CommentGood.objects.filter(comment=comment).count(),
        }
        return JsonResponse(d)


# Pick the thread
@login_required
def pick_up_thread(request, thread_id):
    thread_picked = get_object_or_404(Thread, pk=thread_id)
    if request.method == "POST":
        next_url = request.POST.get('next', None)
        if thread_picked.is_picked:
            thread_picked.is_picked = False
        else:
            thread_picked.is_picked = True
        thread_picked.save()

    if next_url:
        return HttpResponseRedirect(next_url)
    else:
        return redirect('stumee_meeting:index')


# Tag Detail
class TagListView(generic.ListView):
    model = Thread
    context_object_name = 'tag_threads_list'
    template_name = 'stumee_meeting/tag_list.html'

    def get_queryset(self):
        tag_name = self.kwargs['tag_name']
        return Thread.objects.filter(tag__name__in=[tag_name])

    def get_context_data(self, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        context['tag_name'] = self.kwargs['tag_name']
        return context


# The ListView for thread order by make date
class QuestionView(generic.ListView):
    template_name = 'stumee_meeting/question.html'
    context_object_name = 'threads_list'

    def get_queryset(self):
        return Thread.objects.order_by('-make_date')


# The ListView for list of all tag
class AllTagView(generic.ListView):
    template_name = 'stumee_meeting/all_tag.html'
    context_object_name = 'tag_list'

    def get_queryset(self):
        queryset = Tag.objects.all()
        return queryset.annotate(
            thread_count=Count('taggit_taggeditem_items')
        )


class AllUserView(generic.ListView):
    template_name = 'stumee_meeting/all_user.html'
    context_object_name = 'user_list'

    def get_queryset(self):
        queryset = CustomUser.objects.all()
        return queryset
