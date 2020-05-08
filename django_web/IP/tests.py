from django.test import TestCase

# Create your tests here.
from django.http import HttpResponse


def ceshi(request):
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        ip = request.META.get("HTTP_X_FORWARDED_FOR")
    else:
        ip = request.META.get("REMOTE_ADDR")
    return HttpResponse(f'客户端ip:{ip}')
