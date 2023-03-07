from django.core.paginator import Paginator 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django_hosts.resolvers import reverse

from .decorators import mahalla_only
from .models import RequestModel
from .forms import RequestForm
from .helpers import responses_checker
from django.contrib import messages
from notifications.signals import notify
from django.contrib.auth import get_user_model

import pandas as pd 
from .models import Tuman, Mahalla
from password_generator import PasswordGenerator
from django.contrib.auth import get_user_model

User = get_user_model()


pwo = PasswordGenerator()
pwo.excludeschars = "!$%^#$^&*()_+=-`~/><,.;"
pwo.excludeuchars = "ABCDEFGHIJKLMNOPQRSTUVWIXY" # (Optional)

pwo.minlen = 8
pwo.maxlen = 8
paginator_number = 10


# Create your views here.


@login_required(login_url='users/login')
@mahalla_only
def main_view(request):
    context = {'host_name':"www"}

    return render(request=request, template_name="main/main.html", context=context)


#REQUEST LISTS  
@login_required(login_url='users/login')
@mahalla_only
def request_all_list(request):
    context = {"host_name":"www"}
    query_page_num = request.GET.get('page', 1)
    all_request_objects = RequestModel.objects.filter(
        sender=request.user
        ).order_by(
            '-created_at'
        )
    paginator = Paginator(all_request_objects, paginator_number)
    request_objects = paginator.get_page(query_page_num)    
    context['request_objects'] = request_objects
    context['page_name'] = "Barcha so'rovnomalar"
    return render(request=request, template_name='main/request_list.html', context=context)


@login_required(login_url='users/login')
@mahalla_only
def request_finished_list(request):
    context = {"host_name":"www"}
    query_page_num = request.GET.get('page', 1)
    all_request_objects = RequestModel.objects.filter(
        sender=request.user, responses__isnull=False
        ).distinct().order_by(
            '-created_at'
        )
    paginator = Paginator(all_request_objects, paginator_number)
    request_objects = paginator.get_page(query_page_num)    
    context['request_objects'] = request_objects
    context['page_name'] = "Ko'rib chiqilgan so'rovnomalar"

    return render(request=request, template_name='main/request_list.html', context=context)


@login_required(login_url='users/login')
@mahalla_only
def request_not_finished_list(request):
    context = {"host_name":"www"}
    query_page_num = request.GET.get('page', 1)
    all_request_objects = RequestModel.objects.filter(
        sender=request.user, responses__isnull=True
        ).distinct().order_by(
            '-created_at'
        )
    paginator = Paginator(all_request_objects, paginator_number)
    request_objects = paginator.get_page(query_page_num)    
    context['request_objects'] = request_objects
    context['page_name'] = "Ko'rib chiqilmagan so'rovnomalar"

    return render(request=request, template_name='main/request_list.html', context=context)


#REQUEST CREATE AND INFO
@login_required(login_url='users/login')
@mahalla_only
def request_create(request):
    context = {"host_name":"www"}
    if request.method == "GET":
        form = RequestForm()
        context["form"] = form

    elif request.method == "POST":
        form = RequestForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            sender = request.user
            sender_tuman = sender.mahalla.tuman
            sender_tuman_hokimiyat = None
            sender_tuman_qurilish = None
            sender_tuman_kadastr = None

            if data['send_hokimiyat']:
                try:
                    sender_tuman_hokimiyat = User.objects.get(
                        role=User.UserChoice.HOKIMIYAT, tuman=sender_tuman
                    )
                except:
                    pass
 
            if data['send_qurilish']:
                try:
                    sender_tuman_qurilish = User.objects.get(
                        role=User.UserChoice.QURILISH, tuman=sender_tuman
                    )
                except:
                    pass

            if data['send_kadastr']:
                try:
                    sender_tuman_kadastr = User.objects.get(
                        role=User.UserChoice.KADASTR, tuman=sender_tuman
                    )
                except:
                    pass    

            req_obj = RequestModel.objects.create(
                sender=request.user,
                context=data['text_context'],
                address=data['address'],
                image=data['image'],
                hokimiyat_receiver=sender_tuman_hokimiyat,
                kadastr_receiver=sender_tuman_kadastr,
                qurilish_receiver=sender_tuman_qurilish,
            )
            sender = request.user
            recipients = [
                sender_tuman_hokimiyat, 
                sender_tuman_qurilish, 
                sender_tuman_kadastr
            ]
            notification_message = f"Yangi so'rovnoma mavjud (id: {req_obj.id})"
            for recipient in recipients:
                if recipient:
                    notify.send(
                        sender, 
                        recipient=recipient, 
                        verb='Message', 
                        description=notification_message, 
                        request_id=req_obj.pk)

            messages.success(request, 'Yangi so\'rovnoma yaratildi!')
            form = RequestForm()
            context['form'] = form
        else:
            errors = form.errors
            if 'image' in errors.as_data().keys():
                error_message = "Noto'g'ri tipdagi rasm joylandi,\
                     iltimos rasmlarni JPG yoki PNG formatda yuboring!"
                messages.warning(request, error_message)
            else:
                error_message = errors.as_data()['__all__'][0].message
                messages.warning(request, error_message)
            form = RequestForm(request.POST, request.FILES)
            context['errors'] = errors
            context['form'] = form
    return render(request=request, template_name='main/request_create.html', context=context)


@login_required(login_url='users/login')
@mahalla_only
def request_info_view(request, pk):
    context = {'host_name':"www"}
    try:
        req_object = RequestModel.objects.get(pk=pk)
    except:
        return redirect(reverse('main', host='www'))
    #removing notification if there is one
    user_notification_for_requests = request.user.notifications.filter(
            notificationcta__request_id=pk,
            unread=True
        )
    if user_notification_for_requests.count() != 0:
        user_notification_for_request = user_notification_for_requests[0]
        user_notification_for_request.unread = False
        user_notification_for_request.save()
            
    
    response_from_hokim, response_from_kadastr, \
        response_from_qurilish, is_certified = responses_checker(req_object=req_object)
    context['response_from_hokim'] = response_from_hokim
    context['response_from_kadastr'] = response_from_kadastr
    context['response_from_qurilish'] = response_from_qurilish
    context['is_certified'] = is_certified
    context['object'] = req_object

    return render(request=request, template_name='main/request_info.html', context=context)




    # users = User.objects.filter(role=User.UserChoice.KADASTR, username__startswith='nazoratchi')
    # users.update(role=User.UserChoice.NAZORATCHI,)
    # users.delete()
    # print('deleted')
    # for user in users:
    #     mahalla_obj = user.mahalla
    #     tuman_obj = mahalla_obj.tuman
    #     tuman_name = tuman_obj.name.replace('tuman', '').replace(' i', '')
    #     mahalla_name = mahalla_obj.name.replace('MFY', '').replace(' ', '')
    #     user.username = f"{mahalla_name}_{tuman_name}"
    #     user.save()

    # # data = pd.read_csv("tuman_data.csv")
    # new_data = pd.read_csv("nazorat_data.csv")
    # passwords = []
    # usernames = []
    # for tuman_obj in Tuman.objects.all():
    #     tuman_name = tuman_obj.name.replace('tumani', '').replace('tuman', '')\
    #         .replace(' shahar', '').replace(' shahri', '').replace(' sh', '').lower()
        
        
    #     user_name = f"nazoratchi_{tuman_name}"
    #     random_password = pwo.generate()
    
# 
    # # for tuman, mahalla, rais in zip(data['Tuman'], data['Mahalla'], data['Rais']):
    #     # tuman_obj = Tuman.objects.get_or_create(name=tuman)[0]
    #     # mahalla_obj = Mahalla.objects.get_or_create(name=mahalla, tuman=tuman_obj)[0]

    #     # mahalla_name = mahalla.replace(' MFY', '').\
    #     #     replace(" FO'O'BO", '').replace(" mahalla fuqarolar yigini", "").replace(' ', '_').lower()


    #     while True:
    #         if user_name[-1] == ' ':
    #             user_name = user_name[:-1]
    #         elif user_name[1] == ' ':
    #             user_name = user_name[1:]
    #         else:
    #             break
    #     try:
    #         user = User.objects.get(username=user_name)
    #     #     # print(mahalla_obj.name)
    #     #     # print(tuman_obj.name)
    #     #     # print(user.mahalla.name)
    #     #     # print(user.mahalla.tuman.name)
    #         print(user_name)
    #         user_name = f"{user_name}_2"
    #     except: 
    #         pass 
    #     user = User(
    #         username=user_name,
    #         password=random_password,
    #         role=User.UserChoice.NAZORATCHI,
    #         tuman=tuman_obj,
    #     )   
    #     user.set_password(random_password)
    #     user.save()
    #     usernames.append(user_name)
    #     passwords.append(random_password)

    # new_data['nazorat_usernames'] = usernames
    # new_data['nazorat_passwords'] = passwords
    # new_data.to_csv("nazorat_data.csv", index=False)

    
    # # mahalla_obj = Mahalla.objects.all()[0]
    

    # #     if rais != "VAKANT": 
    # #         rais_surname = rais.split(' ')[0]
    # #         rais_firstname = rais.split(' ')[1]
    # #     else:
    # #         rais_firstname = ''
    # #         rais_surname = ''
    # # user = User(username='jamshid', role=User.UserChoice.RAIS, mahalla=mahalla_obj)
    # # user.save()
    # # user.set_password("67?aZyZy")
    # # user.save()
    
    # # users  = User.objects.all()
    # # print(user.is_active)

    # # user.is_active = True
    # # user.save()

    # for user in users:
    #     print(user.__dict__)