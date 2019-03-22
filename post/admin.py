from django.contrib import admin

from .models import Post,Topic,Tag,RelatedURL
from .adminforms import PostAdminForm

# admin.site.register(Post)
# admin.site.register(Topic)
# admin.site.register(Tag)
@admin.register(RelatedURL)
class RelatedURLAdmin(admin.ModelAdmin):
    list_display = ['short_des','url_address']

class RelatedURLInline(admin.StackedInline):
    model = RelatedURL
    extra = 2
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form =PostAdminForm
    # fields = ['title','author','topic_name','tag_name', 'desc','status','is_md','created_date','message']
    inlines = [RelatedURLInline]
    fieldsets = [
        (None, {'fields':[('title','author'),('topic_name','tag_name'),('status','is_md','created_date'),('desc')]}),
        (None, {'fields':['message']})
    ]
    list_display=['title', 'topic_name','status', 'author','created_date']
    # list_display_links = ['topic_name','author']
    list_filter = ['topic_name',]
    search_fields = ['title', 'topic_name__topic_name']
    save_on_top =True
    actions_on_top = True

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['topic_name','is_nav']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
