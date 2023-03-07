from hukumat.models import Response


def responses_checker(req_object):
    responses = Response.objects.filter(request=req_object)
    response_from_hokim = None
    response_from_kadastr = None
    response_from_qurilish = None
    is_certified = False
    if req_object.hokimiyat_receiver != None:
        hokim_obj = req_object.hokimiyat_receiver
        try:
            response_from_hokim = responses.get(sender=hokim_obj)
        except:
            pass

    if req_object.kadastr_receiver != None:
        kadastr_obj = req_object.kadastr_receiver
        try:
            response_from_kadastr = responses.get(sender=kadastr_obj)
        except:
            pass

    if req_object.qurilish_receiver != None:
        qurilish_obj = req_object.qurilish_receiver
        try:
            response_from_qurilish = responses.get(sender=qurilish_obj)
        except:
            pass
    if response_from_hokim:
        if response_from_hokim.is_certified:
            is_certified = True
    if response_from_kadastr:
        if response_from_kadastr.is_certified:
            is_certified = True
    if response_from_qurilish:
        if response_from_qurilish.is_certified:
            is_certified = True
    return response_from_hokim, response_from_kadastr, \
        response_from_qurilish, is_certified