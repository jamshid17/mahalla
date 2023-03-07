from django.shortcuts import render, redirect
from django_hosts.resolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.
def login_view(request):
    #finding out what host are we in and putting it in context
    print(request.user.is_authenticated, "  user authed")
    host = request.get_host()
    if host.startswith('hukumat.'):
        host_name = "hukumat"
    elif host.startswith('nazorat.'):
        host_name = "nazorat"
    else:
        host_name = "www"
    print(host_name, " host name")
    context = {"host_name" : host_name}

    #redirecting if user is authenticated
    if request.user.is_authenticated:
        return redirect(reverse('main', host=host_name))

    if request.method == 'GET':
        return render(request, 'users/login.html', context=context)

    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user_role = request.user.role
            if user_role in ['Rais', 'Hokim yordamchisi']:
                return redirect(reverse('main', host='www'))
            elif user_role == 'Nazoratchi' or request.user.is_superuser:
                return redirect(reverse('main', host='nazorat'))
            else:
                return redirect(reverse('main', host='hukumat'))
                
        else:
            error_message = 'Not\'g\'ri username yoki parol'  # to display error?
            messages.warning(request, error_message)
            return render(request, 'users/login.html', context=context)


def logout_view(request):
    user_role = request.user.role
    is_superuser = request.user.is_superuser
    logout(request=request)
    if user_role in ['Rais', 'Hokim yordamchisi']:
        return redirect(reverse('main', host='www'))
    elif user_role == 'Nazoratchi' or is_superuser:
        return redirect(reverse('main', host='nazorat'))
    else:
        return redirect(reverse('main', host='hukumat'))
    