from django.contrib import admin
from .models import Blog
from .models import BlogManager

class BlogAdmin(admin.ModelAdmin):
   def get_queryset(self, request):
        queryset = BlogManager.get_queryset(self, request)
        return queryset

admin.site.register(Blog, BlogAdmin)
