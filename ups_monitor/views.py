from datetime import datetime
from sre_parse import State
from django.db.models import Max
from django.shortcuts import redirect, render
from django.http import HttpResponse, request
from .models import UPS, StateHistory, ReportHIstory
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .state_ups.datail_telnet import get_detail_ups
from .state_ups.telnet_with_auth import get_state_ups
from django.contrib.auth.decorators import login_required 
from django.core.exceptions import PermissionDenied, EmptyResultSet
from .state_ups.check import check_state, check_detail
from django.contrib.auth import logout

# Create your views here.

def index(request):

    return redirect('/ups')


@login_required
def ups_list(request):
    ups_qs = StateHistory.objects.raw('SELECT * FROM ups_monitor_statehistory group by ups_id HAVING date_add=max(date_add);')
    
    return render(request, 'ups_list.html', {'ups_qs': ups_qs, })
                                               

@login_required
def detail(request, ip):
    try:
        report_qs = ReportHIstory.objects.filter(ups__ip=ip).latest('date_add')
    except :
        ups = UPS.objects.get(ip=ip)
        ReportHIstory(
            ups = ups
        ).save()

    state_qs = StateHistory.objects.filter(ups__ip=ip).latest('date_add')
    report_qs = ReportHIstory.objects.filter(ups__ip=ip).latest('date_add')
    return render(request, 'detail.html', {
        'report_ups': report_qs,
        'ups': state_qs,
        'ip': state_qs.ups.ip,
        'buttom': request.user.has_perm('ups_monitor.add_post')
    })


@api_view(['GET'])
def ups_state_list(request):
    if request.method == 'GET':
        ups_qs = StateHistory.objects.raw('SELECT * FROM ups_monitor_statehistory group by ups_id HAVING date_add=max(date_add);')
        serializer = StateHistorySerializer(ups_qs, context={'request': request}, many=True)
        return Response({'data': serializer.data })


@login_required
@api_view(['GET'])
def check_state_now(request, ip):
    ups = UPS.objects.get(ip=ip)
    state = check_state(ups)
    print(state)
    if state == None:
        raise EmptyResultSet
    serializer = StateHistorySerializer(state, context={'request': request})
    return Response({'data': serializer.data,})


@login_required   
@api_view(['GET'])
def ups_detail(request, ip):
    if request.method == 'GET':
        state_qs = ReportHIstory.objects.filter(ups__ip=ip).latest('date_add')
        serializer = ReportHistorySerializer(state_qs, context={'request': request})
        return Response({'data': serializer.data ,})


@login_required
@api_view(['GET'])
def update_detail(request, ip):
    if not request.user.has_perm('ups_monitor.add_post'):
        print(f"------ {request.user.has_perm('ups_monitor.add_post')}")
        raise PermissionDenied
    if  request.method == 'GET':
        ups = UPS.objects.get(ip=ip)
        detail = check_detail(ups)
        if detail == None:
            raise EmptyResultSet
        print(detail)
        serializer = ReportHistorySerializer(detail, context={'request': request})
        return Response({'data': serializer.data ,})

        

# Test, need delite
def orders_app(request):
    return render(request, 'ups_web/main_app.html')

def detail_ups(request):
    return render(request, "ups_web/detail_ups.html")

