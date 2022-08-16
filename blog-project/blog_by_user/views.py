from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.models import Group
from .models import Blog, BlogManager
from .admin import BlogAdmin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime

def home(request):
    blogs = Blog.objects.all()

    total_views = 0
    for blog in blogs:
        total_views += blog.views_total

    total_registered_users=0
    users = User.objects.all()
    for user in users:
        total_registered_users += 1

    today=datetime.now()
    total_blogs_monthly = 0
    for blog in blogs:
        if blog.pub_date.strftime('%Y-%m-%d') == today.strftime('%Y-%m-%d'):
            total_blogs_monthly += 1

    return render(request, 'home.html', {'blogs':blogs,'total_views':total_views, 'total_registered_users':total_registered_users, 'total_blogs_monthly':total_blogs_monthly})

def userblog(request):

    if request.user.is_authenticated:
        blogs = BlogAdmin.get_queryset(BlogAdmin, request)

        total_views = 0
        for blog in blogs:
            total_views += blog.views_total

        today=datetime.now()

        total_blogs_monthly = 0
        for blog in blogs:
            if blog.pub_date.strftime('%Y-%m-%d') == today.strftime('%Y-%m-%d'):
                total_blogs_monthly += 1

        topicwise_views={}
        trending_blogs={}
        l=len(blogs)
        n=3  #Top n blogs
        top_n_blogs = blogs[:n]

        for blog in blogs[:n]:
            trending_blogs[blog.title]= blog.views_total

        for i in range(len(blogs)):
            if blogs[l-1-i].topic in topicwise_views:
                topicwise_views[blogs[l-1-i].topic] += blogs[l-1-i].views_total
            else:
                topicwise_views[blogs[l-1-i].topic] = blogs[l-1-i].views_total

        return render(request, 'userblog.html', {'userblogs':blogs, 'topicwise_views':topicwise_views, 'trending_blogs':trending_blogs, 'total_views':total_views, 'total_blogs_monthly':total_blogs_monthly})

    else:

        return render(request, 'userblog.html')



def viewblog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.user.is_authenticated:
        return render(request, 'viewblog.html', {'blog':blog})
    else:
        blog.views_total += 1
        blog.save()
        return render(request, 'viewblog.html', {'blog':blog})

@login_required
def adduserblog(request):
    if request.method == 'POST':
        blog = Blog()
        blog.title = request.POST['title']
        blog.topic = request.POST['topic']
        blog.body = request.POST['body']
        blog.pub_date = timezone.datetime.now()
        blog.author = request.user
        blog.save()
        return redirect('userblog')
    else:
        return render(request, 'addblog.html')

@login_required
def edituserblog(request, blog_id):
    if request.method == 'POST':
        blog = get_object_or_404(Blog, pk=blog_id)
        blog.title = request.POST['title']
        blog.topic = request.POST['topic']
        blog.body = request.POST['body']
        blog.pub_date = timezone.datetime.now()
        blog.save()
        return redirect('userblog')
    else:
        blog = get_object_or_404(Blog, pk=blog_id)
        if blog.author == request.user or request.user.is_superuser:
            return render(request, 'editblog.html', {'blog':blog})
        else:
            return redirect('userblog')

@login_required
def deleteuserblog(request, blog_id):
        blog = get_object_or_404(Blog, pk=blog_id)
        if blog.author == request.user or request.user.is_superuser:
            blog.delete()
            return redirect('userblog')
        else:
            return redirect('userblog')

def wrongDetails(request):
    return render(request,'wrongDetails.html')

def chosenUsername(request):
    return render(request,'chosenUsername.html')            
