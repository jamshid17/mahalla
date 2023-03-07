from django.urls import path 
from .views import (
    main_view, 
    request_info_view, 
    request_create, 
    request_all_list, 
    request_not_finished_list, 
    request_finished_list
    )


urlpatterns = [
    path("", main_view, name='main'),
    path("requests/create", request_create, name='request-create'),
    path("requests/info/<pk>", request_info_view, name='request-info'),
    path("requests/all/", request_all_list, name='all-request-list'),
    path("requests/finished", request_finished_list, name='finished-request-list'),
    path("requests/notfinished", request_not_finished_list, name='not-finished-request-list'),
]
