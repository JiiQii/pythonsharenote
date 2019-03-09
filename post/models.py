from django.db import models
from django.utils import timezone
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
import misaka

class Topic(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, 'Normal'),
        (STATUS_DELETE, 'Deleted'),
    )
    topic_name = models.CharField(max_length=30,verbose_name="Topic")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS,verbose_name="Status")
    is_nav = models.BooleanField(default=False, verbose_name="IsNav")
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='Created Time')
    class Meta:
        ordering = ('created_time',)
    def __str__(self):
        return self.topic_name

class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, 'Normal'),
        (STATUS_DELETE, 'Deleted'),
    )
    tag_name = models.CharField(max_length=30,verbose_name="Tag")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="Status")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Created Time")
    def __str__(self):
        return self.tag_name
    class Meta:
        ordering = ['created_time',]

class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, 'Normal'),
        (STATUS_DELETE, 'Deleted'),
        (STATUS_DRAFT, 'Draft'),
    )

    topic_name = models.ForeignKey('Topic',related_name='post_topic',on_delete=False)
    tag_name = models.ManyToManyField('Tag', related_name='post_tags')
    author = models.ForeignKey(User, on_delete=False, verbose_name='Author')
    title = models.CharField(max_length=200,verbose_name='Title')
    desc = models.CharField(max_length=1024, blank=True, verbose_name="Summary")
    message = RichTextUploadingField(verbose_name='Content')
    message_html = models.TextField(editable=False,verbose_name='Cotent_HTML')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='Status')
    is_md = models.BooleanField(default=False, verbose_name='IsMarkDown')
    created_date = models.DateTimeField(default=timezone.now,verbose_name='Created Time')
    published_date = models.DateTimeField(blank=True, null=True,verbose_name='Published Date')

    # def publish(self):
    #     self.published_date = timezone.now()
    #     self.save()
    class Meta:
        verbose_name = verbose_name_plural = "Artical"
        ordering = ('-published_date',)

    def save(self,*args,**kwargs):
        self.published_date = timezone.now()
        if self.is_md:
            self.message_html = misaka.html(self.message)
        else:
            self.message_html = self.message
        super().save(*args,**kwargs)

    def __str__(self):
        return self.title

class RelatedURL(models.Model):
    post = models.ForeignKey(Post, related_name='reflink',on_delete=models.CASCADE,blank=True, null=True)
    short_des = models.CharField(max_length=256)
    url_address = models.URLField()

#
