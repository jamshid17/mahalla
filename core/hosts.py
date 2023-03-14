from django_hosts import patterns, host
from django.conf import settings
from core.settings import DOMAIN_NAME



host_patterns = patterns('',
    host(r'{}'.format(DOMAIN_NAME), settings.ROOT_URLCONF, name='www'),
    host(r'umumiy.{}'.format(DOMAIN_NAME), 'hukumat.urls', name='hukumat'),
    host(r'nazorat.{}'.format(DOMAIN_NAME), 'nazorat.urls', name='nazorat'),
)