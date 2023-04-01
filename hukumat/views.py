from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Response
from .decorators import hukumat_only
from main.models import RequestModel
from django.shortcuts import render, redirect
from django_hosts.resolvers import reverse
from .forms import ResponseForm
from django.db.models import Q
from django.core.paginator import Paginator 
from notifications.signals import notify
from core.settings import GOOGLE_MAP_API_KEY


paginator_number = 10
# Create your views here.
@login_required(login_url="users/login")
@hukumat_only
def main(request):
    context = {"host_name":"hukumat"}
    print(request.user.role, ' dic')
    return render(request, 'hukumat/hukumat.html', context=context)


#REQUEST LISTS  
@login_required(login_url='users/login')
@hukumat_only
def request_all_list(request):
    context = {"host_name":"hukumat"}
    query_page_num = request.GET.get('page', 1)

    all_request_objects = RequestModel.objects.filter(
        Q(hokimiyat_receiver=request.user)|
        Q(kadastr_receiver=request.user)|
        Q(qurilish_receiver=request.user)
    ).order_by('-created_at')
    paginator = Paginator(all_request_objects, paginator_number)
    request_objects = paginator.get_page(query_page_num)    
    
    context['request_objects'] = request_objects
    context['all_requests'] = True
    context['page_name'] = "Barcha so'rovnomalar"

    return render(request=request, template_name='hukumat/request_list.html', context=context)


@login_required(login_url='users/login')
@hukumat_only
def request_finished_list(request):
    context = {"host_name":"hukumat"}
    query_page_num = request.GET.get('page', 1)

    all_request_objects = RequestModel.objects.filter(
        responses__sender=request.user
    )


    paginator = Paginator(all_request_objects, paginator_number)
    request_objects = paginator.get_page(query_page_num)    
    context['request_objects'] = request_objects
    context['all_requests'] = True
    context['page_name'] = "Ko'rib chiqilgan so'rovnomalar"

    return render(request=request, template_name='hukumat/request_list.html', context=context)


@login_required(login_url='users/login')
@hukumat_only
def request_not_finished_list(request):
    context = {"host_name":"hukumat"}
    query_page_num = request.GET.get('page', 1)
    all_request_objects = RequestModel.objects.filter(
        Q(hokimiyat_receiver=request.user)|
        Q(kadastr_receiver=request.user)|
        Q(qurilish_receiver=request.user),
        ~Q(responses__sender=request.user),
    ).order_by('-created_at')
    paginator = Paginator(all_request_objects, paginator_number)
    request_objects = paginator.get_page(query_page_num)    
    context['request_objects'] = request_objects
    context['all_requests'] = True
    context['page_name'] = "Ko'rib chiqilmagan so'rovnomalar"

    return render(request=request, template_name='hukumat/request_list.html', context=context)


@login_required(login_url='users/login')
@hukumat_only
#_response_update
def request_info_view(request, pk):
    context = {'host_name':"hukumat"}
    try:
        req_object = RequestModel.objects.get(pk=pk)
    except:
        return redirect(reverse('main', host='hukumat'))
    context['object'] = req_object
    #finding response
    user_responses = Response.objects.filter(sender=request.user, request=req_object)
    if user_responses.count() == 0:
        user_response = None
    else:
        user_response = user_responses[0]
    #removing notification if there is one
    user_notification_for_requests = request.user.notifications.filter(
            notificationcta__request_id=pk,
            unread=True
        )
    if user_notification_for_requests.count() != 0:
        user_notification_for_request = user_notification_for_requests[0]
        user_notification_for_request.unread = False
        user_notification_for_request.save()
            
    

    if request.method == 'GET':
        form = ResponseForm()
    elif request.method == 'POST':
        if not user_response:
            form = ResponseForm(request.POST, request.FILES)
            if form.is_valid():
                res_obj = form.save(commit=False)
                res_obj.sender = request.user
                res_obj.request = req_object
                res_obj.clean() 
                res_obj.save()    
                sender = request.user
                recipient=req_object.sender
                notification_message = f"Yangi javob mavjud (id: {req_object.id}) ({sender.role}dan)"
                notify.send(
                    sender,
                    recipient=recipient,
                    verb='Message', 
                    description=notification_message,
                    request_id=req_object.pk
                )
                user_response = res_obj
        else:
            form = None

    context['map_key'] = GOOGLE_MAP_API_KEY
    context['user_response'] = user_response
    context['form'] = form

    return render(request=request, template_name='hukumat/request_info.html', context=context)
