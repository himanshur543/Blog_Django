from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('/userblog')
        else:
            #return render(request, 'home.html', {'error':'Username or Password is incorrect'})
            return redirect('wrongDetails')
    else:
        return redirect('home')

def signup(request):
        if request.method == 'POST':

            if request.POST['password'] == request.POST['confirmpassword']:
                try:
                    user = User.objects.get(username=request.POST['username'])
                    return redirect('chosenUsername')
                except User.DoesNotExist:
                    user = User.objects.create_user(request.POST['username'], password=request.POST['password'], is_staff=True)
                    user.first_name = request.POST['firstname']
                    user.last_name = request.POST['lastname']
                    user.save()
                    permission_1 = Permission.objects.get(name='Can view blog')
                    permission_2 = Permission.objects.get(name='Can add blog')
                    permission_3 = Permission.objects.get(name='Can change blog')
                    permission_4 = Permission.objects.get(name='Can delete blog')
                    user.user_permissions.add(permission_1)
                    user.user_permissions.add(permission_2)
                    user.user_permissions.add(permission_3)
                    user.user_permissions.add(permission_4)
                    user.save()
                    return redirect('home')
            else:
                return redirect('home')

        else:
            return redirect('home')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
