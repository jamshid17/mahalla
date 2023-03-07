from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    main, 
    request_all_list, 
    request_finished_list, 
    request_not_finished_list, 
    request_info_view)

urlpatterns = [
    path("", main, name='main'),
    path('users/', include('users.urls')), 
    path("requests/all", request_all_list, name='all-request-list'),
    path("requests/finished", request_finished_list, name='finished-request-list'),
    path("requests/notfinished", request_not_finished_list, name='not-finished-request-list'),
    path("requests/info/<pk>", request_info_view, name='request-info'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)