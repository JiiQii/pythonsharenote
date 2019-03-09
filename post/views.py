from .models import Post, Tag, Topic,RelatedURL
from django.utils import timezone
from django.views.generic import (View,TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)
from django.core.paginator import Paginator
from django.shortcuts import render


def coming(request):
    return render(request,'coming.html')

class CommonMixinView(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = Topic.objects.all()
        return context

class TagsMixinView(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context

class BasePostsView(TagsMixinView,CommonMixinView,ListView):
    model = Post
    template_name = "post_list.html" # Quse
    context_object_name = 'posts'
    paginate_by = 7

class IndexView(BasePostsView):
    pass

class TopicPostsView(BasePostsView):
    def get_queryset(self):
        qs = super(TopicPostsView, self).get_queryset()
        to_id = self.kwargs.get('topic_id')
        qs = qs.filter(topic_name_id=to_id)
        return qs

class TagPostsView(BasePostsView):

    def get_queryset(self):
        ta_id = self.kwargs.get('tag_id')
        try:
            tag = Tag.objects.get(id=ta_id)
        except Tag.DoesNotExist:
            return []
        posts = tag.post_tags.all()
        return posts


class PostDetailView(TagsMixinView,CommonMixinView,DetailView):
    model = Post
    tamplate_name = 'post_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_pk = self.kwargs.get('pk')
        try:
            post = Post.objects.get(pk=post_pk)
        except Post.DoseNotExist:
            return []
        context['links'] = post.reflink.all()
        return context
