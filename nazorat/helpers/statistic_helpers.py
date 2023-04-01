from http.client import responses
from urllib import request
from main.models import RequestModel, Mahalla, Tuman
from hukumat.models import Response
from datetime import datetime
from django.utils.timezone import make_aware
from django.contrib.auth import get_user_model

User = get_user_model()


def main_stats_calculator(request_objects):
    main_stats = {}
    all_request_count = request_objects.count()
    not_finished_request_count = request_objects.filter(responses__isnull=True).count()
    finished_request_count = all_request_count - not_finished_request_count
    legal_request_count = request_objects.filter(responses__is_certified=True).distinct().count()
    illegal_request_count = request_objects.filter(responses__is_certified=False).distinct().count()

    
    if all_request_count == 0:
        finished_percentage = "-"
    else:   
        finished_percentage = int(100*(finished_request_count/all_request_count))
    
    late_responses_count = request_objects.filter(responses__is_late=True).distinct().count() 
    main_stats['all_request_count'] = all_request_count
    main_stats['finished_request_count'] = finished_request_count
    main_stats['legal_request_count'] = legal_request_count
    main_stats['illegal_request_count'] = illegal_request_count
    main_stats['not_finished_request_count'] = not_finished_request_count
    main_stats['finished_percentage'] = finished_percentage
    main_stats['late_responses_count'] = late_responses_count

    return main_stats


def deadline_stats_calculator(request_objects):
    not_finished_requests = request_objects.filter(responses__isnull=True)
    deadlines = {
        "zero_day_left_requests": 0,
        "one_day_left_requests": 0,
        "two_day_left_requests": 0,
        "three_day_left_requests": 0,
        "four_day_left_requests": 0,
        "five_day_left_requests": 0,
    }
    dt_now = make_aware(datetime.now())
    for not_finished_request in not_finished_requests:
        request_created_at = not_finished_request.created_at
        difference_days = 5 - (dt_now - request_created_at).days
        if difference_days == 0:
            deadlines["zero_day_left_requests"] += 1
        if difference_days == 1:
            deadlines["one_day_left_requests"] += 1
        if difference_days == 2:
            deadlines["two_day_left_requests"] += 1
        if difference_days == 3:
            deadlines["three_day_left_requests"] += 1
        if difference_days == 4:
            deadlines["four_day_left_requests"] += 1
        if difference_days == 5:
            deadlines["five_day_left_requests"] += 1
            
    return deadlines

def table_stats_mahalla_calculator(nazoratchi):
    request_objs = RequestModel.objects.all()
    
    nazoratchi_tuman = nazoratchi.tuman
    all_stats = []
    mahalla_objects = Mahalla.objects.filter(tuman=nazoratchi_tuman)
    for mahalla_object in mahalla_objects:
        mahalla_request_objs = request_objs.filter(sender__mahalla=mahalla_object)
        main_stats = main_stats_calculator(request_objects=mahalla_request_objs)
        deadline_stats = deadline_stats_calculator(request_objects=mahalla_request_objs)
        full_stats = {**main_stats, **deadline_stats}
        all_stats.append({
            'place_name':mahalla_object.name,
            'place_id':mahalla_object.id,
            'place_stats':full_stats,
        })
    
    return all_stats


def table_stats_tuman_calculator():
    request_objs = RequestModel.objects.all()
    all_stats = []
    tuman_objects = Tuman.objects.all()
    for tuman_object in tuman_objects:
        tuman_request_objs = request_objs.filter(sender__mahalla__tuman=tuman_object)
        main_stats = main_stats_calculator(request_objects=tuman_request_objs)
        deadline_stats = deadline_stats_calculator(request_objects=tuman_request_objs)
        full_stats = {**main_stats, **deadline_stats}
        all_stats.append({
            'place_name':tuman_object.name,
            'place_id':tuman_object.id,
            'place_stats':full_stats,
        })
    return all_stats



def monthly_stats_calculator(request_objs, start_range, end_rage):
    stats = {}
    request_objs = request_objs.filter(
        created_at__gte=start_range,
        created_at__lte=end_rage,
    )
    requests_sent_by_rais = request_objs.filter(
        sender__role = User.UserChoice.RAIS 
    )
    requests_sent_by_hokim_yordamchisi = request_objs.filter(
        sender__role = User.UserChoice.HOKIM_YORDAMCHISI 
    )
    requests_sent_to_hokimiyat = request_objs.filter(
        hokimiyat_receiver__isnull=False 
    )
    requests_sent_to_kadastr = request_objs.filter(
        kadastr_receiver__isnull=False 
    )
    requests_sent_to_qurilish = request_objs.filter(
        qurilish_receiver__isnull=False 
    )
    requests_certified = request_objs.filter(
        responses__is_certified=True
    ).distinct()
    requests_not_certified = request_objs.filter(
        responses__is_certified=False
    ).distinct()

    stats['count'] = request_objs.count()
    stats['sent_by_rais'] = requests_sent_by_rais.count()
    stats['sent_by_hokim_yordamchisi'] = requests_sent_by_hokim_yordamchisi.count()
    stats['sent_to_hokimiyat'] = requests_sent_to_hokimiyat.count()
    stats['sent_to_kadastr'] = requests_sent_to_kadastr.count()
    stats['sent_to_qurilish'] = requests_sent_to_qurilish.count()
    stats['requests_certified'] = requests_certified.count()
    stats['requests_not_certified'] = requests_not_certified.count()
    
    return stats