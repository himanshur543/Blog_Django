from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('userblog/',views.userblog, name='userblog'),
    path('<int:blog_id>/',views.viewblog, name='viewblog'),
    path('userblog/addblog',views.adduserblog, name='addblog'),
    path('userblog/editblog/<int:blog_id>/',views.edituserblog, name='editblog'),
    path('userblog/deleteblog/<int:blog_id>/',views.deleteuserblog, name='deleteblog'),
    path('wrongDetails',views.wrongDetails, name='wrongDetails'),
    path('chosenUsername',views.chosenUsername, name='chosenUsername'),

]
