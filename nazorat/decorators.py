from functools import wraps
from django.shortcuts import redirect
from django_hosts.resolvers import reverse

def nazoratchi_only(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
            user_role = request.user.role
            if user_role in ['Nazoratchi'] or request.user.is_superuser:
                return function(request, *args, **kwargs)
            elif user_role in ['Rais', 'Hokim yordamchisi']:
                return redirect(reverse('main', host='www'))
            else:
                return redirect(reverse('main', host='hukumat'))


    return wrap