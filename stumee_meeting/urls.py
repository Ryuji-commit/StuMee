from django.urls import path

from . import views

app_name = 'stumee_meeting'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:thread_id>', views.thread, name='thread'),
    path('ask', views.post_thread, name='post_thread'),
    path('<int:thread_id>/thread_good', views.add_good_for_thread, name='thread_good'),
    path('<int:comment_id>/comment_good', views.add_good_for_comment, name='comment_good'),
    path('tagged/<str:tag_name>', views.TagListView.as_view(), name='tag_filter'),
    path('question', views.QuestionView.as_view(), name='question'),
    path('tags', views.AllTagView.as_view(), name='tags'),
    path('<int:thread_id>/pickup', views.pick_up_thread, name='thread_pickup'),
    path('search', views.SearchThreadView.as_view(), name='thread_search'),
]
