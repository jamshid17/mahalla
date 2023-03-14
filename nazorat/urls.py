from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    main,
    all_requests,
    finished_requests,
    not_finished_requests,
    late_answered_requests,
    days_left_requests,
    request_detail,
    period_stats,
    period_requests
)
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", main, name='main'),
    path('users/', include('users.urls')), 
    path("allrequests/", all_requests, name='all-requests'),
    path("finished-requests/", finished_requests, name='finished-requests'),
    path("not-finished-requests/", not_finished_requests, name='not-finished-requests'),
    path("late-answered-requests/", late_answered_requests, name='late-answered-requests'),
    path("days-left-requests/", days_left_requests, name='days-left-requests'),
    path("request-detail/<pk>", request_detail, name='request-detail'),
    path("period_stats/", period_stats, name='period-stats'),
    path("period_requests/", period_requests, name='periodic-requests'),


    # period-stats

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)