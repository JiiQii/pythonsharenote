from .models import Post, Tag, Topic,RelatedURL
from django.utils import timezone
from django.views.generic import (View,TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q, F


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
    paginate_by = 10

    def get_queryset(self):
        order = self.request.GET.get('orderby', '-published_date')
        new_context = Post.objects.filter(status=Post.STATUS_NORMAL).order_by(order)
        return new_context

    def get_context_data(self, **kwargs):
        context = super(BasePostsView, self).get_context_data(**kwargs)
        context['orderby'] = self.request.GET.get('orderby', 'published_date')
        context['d_orderby'] = self.request.GET.get('orderby', '-published_date')
        return context

class IndexView(BasePostsView):
    def get_queryset(self):
        query = self.request.GET.get('query')
        qs = super(IndexView, self).get_queryset()
        if not query:
            return qs
        return qs.filter(Q(title__icontains=query) | Q(tag_name__tag_name__icontains=query))

    def get_context_data(self,**kwargs):
        query = self.request.GET.get('query')
        return super(IndexView,self).get_context_data(query=query)

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

# class SearchView(BasePostsView):
#     def get_context_data(self):
#         context = super().get_context_data()
#         context.update({
#             'keyword': self.request.GET.get('keyword', '')
#         })
#         return context
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         keyword = self.request.GET.get('keyword')
#         # if not keyword:
#         #     return queryset
#         # return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))
#         if keyword:
#             query_list = query.split()
#             queryset = queryset.filter(
#                 reduce(operator.and_,
#                        (Q(title__icontains=keyword) for keyword in query_list)) |
#                 reduce(operator.and_,
#                        (Q(tag_name__icontains=keyword) for keyword in query_list))
#             )
#
#         return queryset

# class SearchView(BasePostsView):


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data()
    #     context.update({
    #         'keyword': self.request.GET.get('keyword', '')
    #     })
    #     return context
    #
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     keyword = self.request.GET.get('keyword')
    #     if not keyword:
    #         return queryset
    #     return queryset.filter(Q(title__icontains=keyword))

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
