from django.urls import path
from .views import (IndexView,PostDetailView,TagPostsView,TopicPostsView,coming)

urlpatterns =[
    path('',IndexView.as_view(),name='index'),
    path('topic/<int:topic_id>/',TopicPostsView.as_view(),name='topic_posts'),
    path('tag/<int:tag_id>/',TagPostsView.as_view(),name='tag_posts'),
    path('post/<int:pk>/',PostDetailView.as_view(), name='post_detail'),
    path('coming/',coming, name='coming'),

]
