from django.shortcuts import render, redirect
from django_hosts.resolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from pandas import date_range 

from .decorators import nazoratchi_only
from main.models import RequestModel, Mahalla, Tuman
from .forms import RangeForm
from hukumat.models import Response
from datetime import datetime, timezone, timedelta
from django.utils.timezone import make_aware
from main.helpers import responses_checker
from .helpers.statistic_helpers import *


request_objs = RequestModel.objects.all()
response_objs = Response.objects.all()

paginator_number = 10

# NAZORAT VIEWS
@login_required(login_url='users/login')
@nazoratchi_only
def main(request):
    context = {
        'host_name':'nazorat'
    }
    user = request.user
    request_objs = RequestModel.objects.all()
    if user.role == 'Nazoratchi':
        nazoratchi_tumani = user.tuman
        request_objs = request_objs.filter(sender__mahalla__tuman=nazoratchi_tumani)
    #main_stats
    main_stats = main_stats_calculator(request_objects=request_objs)
    context = {**context, **main_stats}
    #deadline_stats    
    deadline_stats = deadline_stats_calculator(request_objects=request_objs)
    context = {**context, **deadline_stats}
    is_tuman_scale = False
    is_viloyat_scale = False
    
    if user.role == "Nazoratchi":
        is_tuman_scale = True
        table_stats = table_stats_mahalla_calculator(user)
    else:
        is_viloyat_scale = True
        table_stats = table_stats_tuman_calculator()
    context['is_tuman_scale'] = is_tuman_scale
    context['is_viloyat_scale'] = is_viloyat_scale
    context['table_stats'] = table_stats
    return render(request, template_name='nazorat/main.html', context=context)    


@login_required(login_url='users/login')
@nazoratchi_only
def all_requests(request):
    query_tuman_id = request.GET.get('tuman_id', None)
    query_mahalla_id = request.GET.get('mahalla_id', None)
    query_page_num = request.GET.get('page', 1)
    context = {
        'host_name':'nazorat'
    }
    tuman_object = None
    if query_tuman_id and query_tuman_id.isdigit():
        tuman_object = Tuman.objects.get(id=query_tuman_id)
        context['place_name'] = tuman_object.name

    mahalla_object = None
    if query_mahalla_id and query_mahalla_id.isdigit():
        mahalla_object = Mahalla.objects.get(id=query_mahalla_id)
        context['place_name'] = mahalla_object.name 

    user = request.user
    
    if user.role == "Nazoratchi":
        nazoratchi_tumani = user.tuman
        request_objs = RequestModel.objects.filter(sender__mahalla__tuman=nazoratchi_tumani)
        if mahalla_object:
            request_objs = request_objs.filter(sender__mahalla=mahalla_object)
            
    else:
        request_objs = RequestModel.objects.all()
        if tuman_object:
            request_objs = request_objs.filter(sender__mahalla__tuman=tuman_object)
    
    request_objs = request_objs.order_by('-created_at')
    paginator = Paginator(request_objs, paginator_number)
    request_objects = paginator.get_page(query_page_num)  
    context['page_name'] = "Barcha so'rovnomalar"
    context['request_objects'] = request_objects
    return render(request, template_name='nazorat/request_list.html', context=context)    


@login_required(login_url='users/login')
@nazoratchi_only
def finished_requests(request):
    query_tuman_id = request.GET.get('tuman_id', None)
    query_mahalla_id = request.GET.get('mahalla_id', None)
    query_page_num = request.GET.get('page', 1)
    context = {
        'host_name':'nazorat'
    }

    tuman_object = None
    if query_tuman_id and query_tuman_id.isdigit():
        tuman_object = Tuman.objects.get(id=query_tuman_id)
        context['place_name'] = tuman_object.name
    mahalla_object = None
    if query_mahalla_id and query_mahalla_id.isdigit():
        mahalla_object = Mahalla.objects.get(id=query_mahalla_id)
        context['place_name'] = mahalla_object.name 

    user = request.user
    request_objs = RequestModel.objects.filter(responses__isnull=False).distinct()
    
    if user.role == "Nazoratchi":
        nazoratchi_tumani = user.tuman
        request_objs = request_objs.filter(sender__mahalla__tuman=nazoratchi_tumani)
        if mahalla_object:
            request_objs = request_objs.filter(sender__mahalla=mahalla_object)
    elif tuman_object:
        request_objs = request_objs.filter(sender__mahalla__tuman=tuman_object)

    request_objs = request_objs.order_by('-created_at')
    paginator = Paginator(request_objs, paginator_number)
    request_objects = paginator.get_page(query_page_num)  
    context['page_name'] = "Javob berilgan so'rovnomalar"
    context['request_objects'] = request_objects
    return render(request, template_name='nazorat/request_list.html', context=context)    


@login_required(login_url='users/login')
@nazoratchi_only
def late_answered_requests(request):
    query_tuman_id = request.GET.get('tuman_id', None)
    query_mahalla_id = request.GET.get('mahalla_id', None)
    query_page_num = request.GET.get('page', 1)
    context = {
        'host_name':'nazorat'
    }

    tuman_object = None
    if query_tuman_id and query_tuman_id.isdigit():
        tuman_object = Tuman.objects.get(id=query_tuman_id)
        context['place_name'] = tuman_object.name
    mahalla_object = None
    if query_mahalla_id and query_mahalla_id.isdigit():
        mahalla_object = Mahalla.objects.get(id=query_mahalla_id)
        context['place_name'] = mahalla_object.name 

    user = request.user
    request_objs = RequestModel.objects.filter(responses__is_late=True).distinct()
    if user.role == "Nazoratchi":
        nazoratchi_tumani = user.tuman
        request_objs = request_objs.filter(sender__mahalla__tuman=nazoratchi_tumani)
        if mahalla_object:
            request_objs = request_objs.filter(sender__mahalla=mahalla_object)
    elif tuman_object:
        request_objs = request_objs.filter(sender__mahalla__tuman=tuman_object)

    request_objs = request_objs.order_by('-created_at')
    paginator = Paginator(request_objs, paginator_number)
    request_objects = paginator.get_page(query_page_num)  
    context['page_name'] = "Muddati buzilib javob berilgan so'rovnomalar"
    context['request_objects'] = request_objects
    return render(request, template_name='nazorat/request_list.html', context=context)    



@login_required(login_url='users/login')
@nazoratchi_only
def not_finished_requests(request):
    query_tuman_id = request.GET.get('tuman_id', None)
    query_mahalla_id = request.GET.get('mahalla_id', None)
    query_page_num = request.GET.get('page', 1)
    
    context = {
        'host_name':'nazorat'
    }    
    tuman_object = None
    if query_tuman_id and query_tuman_id.isdigit():
        tuman_object = Tuman.objects.get(id=query_tuman_id)
        context['place_name'] = tuman_object.name
    mahalla_object = None
    if query_mahalla_id and query_mahalla_id.isdigit():
        mahalla_object = Mahalla.objects.get(id=query_mahalla_id)
        context['place_name'] = mahalla_object.name 

    user = request.user
    request_objs = RequestModel.objects.filter(responses__isnull=True).distinct()

    if user.role == "Nazoratchi":
        nazoratchi_tumani = user.tuman
        request_objs = request_objs.filter(sender__mahalla__tuman=nazoratchi_tumani)
        if mahalla_object:
            request_objs = request_objs.filter(sender__mahalla=mahalla_object)
    elif tuman_object:
        request_objs = request_objs.filter(sender__mahalla__tuman=tuman_object)

    request_objs = request_objs.order_by('-created_at')
    paginator = Paginator(request_objs, paginator_number)
    request_objects = paginator.get_page(query_page_num)  
    context['page_name'] = "Javob berilmagan so'rovnomalar"
    context['request_objects'] = request_objects
    return render(request, template_name='nazorat/request_list.html', context=context)    


@login_required(login_url='users/login')
@nazoratchi_only
def days_left_requests(request):
    context = {
        'host_name':'nazorat'
    }    
    query_tuman_id = request.GET.get('tuman_id', None)
    query_mahalla_id = request.GET.get('mahalla_id', None)
    query_days_left = request.GET.get('days', "0")
    query_page_num = request.GET.get('page', 1)
    
    if not query_days_left.isdigit():
        query_days_left = 0
    else:
        query_days_left = int(query_days_left)

    context['days_left'] = query_days_left
    tuman_object = None
    if query_tuman_id and query_tuman_id.isdigit():
        tuman_object = Tuman.objects.get(id=query_tuman_id)
        context['place_name'] = tuman_object.name
    mahalla_object = None
    if query_mahalla_id and query_mahalla_id.isdigit():
        mahalla_object = Mahalla.objects.get(id=query_mahalla_id)
        context['place_name'] = mahalla_object.name 
    user = request.user
    request_objs = RequestModel.objects.filter(responses__isnull=True).distinct()
 
    if user.role == "Nazoratchi":
        nazoratchi_tumani = user.tuman
        request_objs = request_objs.filter(sender__mahalla__tuman=nazoratchi_tumani)
        if mahalla_object:
            request_objs = request_objs.filter(sender__mahalla=mahalla_object)
    elif tuman_object:
        request_objs = request_objs.filter(sender__mahalla__tuman=tuman_object)

    #filtering by days left     
    time_now = make_aware(datetime.now())
    first_range_date = time_now - timedelta(days=6-query_days_left)
    second_range_date = time_now - timedelta(days=5-query_days_left)
    request_objs = request_objs.filter(
        created_at__gt=first_range_date, 
        created_at__lte=second_range_date
    ).order_by('-created_at')

    paginator = Paginator(request_objs, paginator_number)
    request_objects = paginator.get_page(query_page_num)  
    context['page_name'] = f"{query_days_left} kun qolgan so'rovnomalar"
    context['request_objects'] = request_objects

    return render(request, template_name='nazorat/request_list.html', context=context)   


@login_required(login_url='users/login')
@nazoratchi_only
def request_detail(request, pk):
    context = {'host_name':"nazorat"}
    try:
        req_object = RequestModel.objects.get(pk=pk)
    except:
        return redirect(reverse('main', host='nazorat'))
    response_from_hokim, response_from_kadastr, \
        response_from_qurilish, is_certified  = responses_checker(req_object=req_object)
    context['response_from_hokim'] = response_from_hokim
    context['response_from_kadastr'] = response_from_kadastr
    context['response_from_qurilish'] = response_from_qurilish
    context['is_certified'] = is_certified
    context['object'] = req_object
    return render(request=request, template_name='nazorat/request_info.html', context=context)
 

@login_required(login_url='users/login')
@nazoratchi_only
def period_stats(request):
    context = {'host_name':"nazorat"}

    if request.method == "GET":
        form = RangeForm()
        stats = None
    if request.method == "POST":
        
        form = RangeForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            start_range = make_aware(
                datetime.combine(form_data['start_range'], 
                datetime.min.time())
            )
            end_range = make_aware(
                datetime.combine(form_data['end_range'], 
                datetime.min.time())
                )
            request_objs = RequestModel.objects.all()
            if request.user.role == 'Nazoratchi':
                nazoratchi_tumani = request.user.tuman
                request_objs = request_objs.filter(sender__mahalla__tuman=nazoratchi_tumani)
            stats = monthly_stats_calculator(request_objs, start_range, end_range)

    context['form'] = form
    context['stats'] = stats

    return render(
        request=request, 
        template_name='nazorat/periodical_stats.html', 
        context=context
    )

 
@login_required(login_url='users/login')
@nazoratchi_only
def period_requests(request):
    context = {
        "host_name":"nazorat"
    }
    query_rais = request.GET.get('rais', False)
    query_hokim_helper = request.GET.get('hokim_yordamchisi', False)
    query_hokim = request.GET.get('hokimga', False)
    query_qurilish = request.GET.get("Qurilish bo'limiga", False)
    query_kadastr = request.GET.get(' Kadastr agentligiga', False)
    query_certified = request.GET.get('tasdiqlangan', False)
    query_not_certified = request.GET.get('tasdiqlanmagan', False)
    query_start_date = request.GET.get('start_date', '2023-01-01')
    query_end_date = request.GET.get('end_date', '2030-12-31')
    query_page_num = request.GET.get('page', 1)
    
    #filtering request objects
    request_objs = RequestModel.objects.filter(
        created_at__range=[query_start_date, query_end_date], 
    )
    request_user = request.user 
    if request_user.role == User.UserChoice.NAZORATCHI:
        request_objs = request_objs.filter(
            sender__mahalla__tuman=request_user.tuman,
        )
    if query_rais:
        request_objs = request_objs.filter(sender__role=User.UserChoice.RAIS)
    if query_hokim_helper:
        request_objs = request_objs.filter(sender__role=User.UserChoice.HOKIM_YORDAMCHISI) 
    if query_hokim:
        request_objs = request_objs.filter(hokimiyat_receiver__isnull=False)
    if query_kadastr:
        request_objs = request_objs.filter(kadastr_receiver__isnull=False)
    if query_qurilish:
        request_objs = request_objs.filter(qurilish_receiver__isnull=False)
    if query_certified:
        request_objs = request_objs.filter(responses__is_certified=True).distinct()
    if query_not_certified:
        request_objs = request_objs.filter(responses__is_certified=False).distinct()

    request_objs = request_objs.order_by('-created_at')
    paginator = Paginator(request_objs, paginator_number)
    request_objs = paginator.get_page(query_page_num)  

    context['page_name'] = "Taqvimiy statistika"
    context['request_objects'] = request_objs
    return render(request, 'nazorat/request_list.html', context=context)
