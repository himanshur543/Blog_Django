from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import admin

TOPIC_CHOICES = (
    ('','Choose Topic'),
    ('World', 'World'),
    ('Technology', 'Technology'),
    ('Design', 'Design'),
    ('Culture', 'Culture'),
    ('Business', 'Business'),
    ('Politics', 'Politics'),
    ('Opinion', 'Opinion'),
    ('Science', 'Science'),
    ('Health', 'Health'),
    ('Style', 'Style'),
    ('Travel', 'Travel'),
    ('Life', 'Life'),
)

class BlogManager(models.Manager):
    def get_queryset(self, request):
        query = Blog.objects.filter(author=request.user)
        if request.user.is_superuser:
            query = Blog.objects.all()
        return query


class Blog(models.Model):
        author = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
        title = models.CharField(max_length=200)
        topic = models.CharField(max_length=200, choices=TOPIC_CHOICES, default=0)
        pub_date = models.DateTimeField(auto_now_add=True)
        body = models.TextField()
        views_total = models.IntegerField(default=1)

        class Meta:
            ordering = ['-views_total']

        def __str__(self):
            return self.title

        def summary(self):
            res = len(self.body.split())
            count = 0
            location = 0
            if res<=10:
                return (self.body + "...")

            else:
                for char in self.body:
                    location+=1
                    if char.isspace():
                        count+=1
                        if count==10:
                            return (self.body[:location-1] + "...")

        def pub_date_pretty(self):
            return self.pub_date.strftime('%b %e %Y')

        def titleInShort(self):
            if len(self.title)<=10:
                return self.title
            else:
                return (self.title[:10] + "...")

#
# class BlogAdminView(admin.ModelAdmin):
#
#     def get_queryset(self, request):
#         qs = super(BlogAdmin, self).get_queryset(request)
#         if request.user.is_superuser:
#             return qs
#         return qs.filter(author=request.user)
