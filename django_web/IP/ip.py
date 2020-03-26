#!/usr/bin/env python
# coding=utf-8
from django.http import HttpResponse


def get_ip(request):
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        ip = request.META.get("HTTP_X_FORWARDED_FOR")
    else:
        ip = request.META.get("REMOTE_ADDR")
    return HttpResponse(ip)
