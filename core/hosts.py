from django_hosts import patterns, host
from django.conf import settings


host_patterns = patterns('',
    host(r'localhost:8000', settings.ROOT_URLCONF, name='www'),
    host(r'umumiy.localhost:8000', 'hukumat.urls', name='hukumat'),
    host(r'nazorat.localhost:8000', 'nazorat.urls', name='nazorat'),

)