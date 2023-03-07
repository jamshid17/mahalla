from functools import wraps
from django.shortcuts import redirect
from django_hosts.resolvers import reverse

def mahalla_only(function):
  @wraps(function)
  def wrap(request, *args, **kwargs):
        user_role = request.user.role
        print(request.user)
        if user_role in ['Rais', 'Hokim yordamchisi']:
            return function(request, *args, **kwargs)
        else:
            return redirect(reverse('all-request-list', host='hukumat'))


  return wrap