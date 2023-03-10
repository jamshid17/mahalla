from django import template
from datetime import datetime
from django.utils.timezone import make_aware
# from django.db.models import Q


register = template.Library()

@register.filter(name="page_replacer")
def page_replacer(url_path):
    if 'page=' in url_path:
        url_path = url_path.split('page=')[0]
            
    return url_path

@register.filter(name="days_left_calculator")
def days_left_calculator(request_obj, request):
    responses_from_request_user = request_obj.responses.filter(sender=request.user)
    if responses_from_request_user.count() != 0:
        return 'Javob berilgan'
    else:
        dt_now = make_aware(datetime.now())
        difference_days = 5 - (dt_now - request_obj.created_at).days      
        if difference_days > 0:
            return f"{difference_days}  kun qolgan"
        return "Muddati buzilgan"            
