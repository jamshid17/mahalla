from functools import wraps
from django.shortcuts import redirect
from django_hosts.resolvers import reverse
from django.contrib.auth import authenticate, login, logout

def hukumat_only(function):
  @wraps(function)
  def wrap(request, *args, **kwargs):
        user_role = request.user.role
        if user_role in ['Rais', 'Hokim yordamchisi'] or request.user.is_superuser:
            return redirect(reverse('all-request-list', host='www'))
        else:
            return function(request, *args, **kwargs)
  return wrap