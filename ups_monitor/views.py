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
from django.contrib.auth.decorators import login_required 
from django.core.exceptions import PermissionDenied

# Create your views here.


def index(request):

    return redirect('/ups')


@login_required
def ups_list(request):
    ups_qs = StateHistory.objects.raw('SELECT * FROM ups_monitor_statehistory group by ups_id HAVING date_add=max(date_add);')
    
    return render(request, 'ups_list.html', {'ups_qs': ups_qs})


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
    """
    List  customers, or create a new customer.
    """
    if request.method == 'GET':
        ups_qs = StateHistory.objects.raw('SELECT * FROM ups_monitor_statehistory group by ups_id HAVING date_add=max(date_add);')
        serializer = StateHistorySerializer(ups_qs, context={'request': request}, many=True)
        return Response({'data': serializer.data })


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
    elif  request.method == 'GET':
        ups = UPS.objects.get(ip=ip)
        
        detail = get_detail_ups(login=ups.login, password=ups.password, host=ups.ip, port=ups.port)
        
        state_qs = ReportHIstory(
            ups=ups,
            model = detail.model,
            voltage_battary = detail.voltage_battary,
            report_selftest = detail.report_selftest,
            made_date = detail.made_date,
            last_date_battary_replacement = detail.last_date_battary_replacement,
            serial_number = detail.serial_number,
        ).save()

        #state_qs = ReportHIstory.objects.filter(ups__ip=ip).latest('date_add')
        serializer = ReportHistorySerializer(state_qs, context={'request': request})
        return Response({'data': serializer.data ,})

        

# Test, need delite
def orders_app(request):
    return render(request, 'ups_web/main_app.html')

def detail_ups(request):
    return render(request, "ups_web/detail_ups.html")

