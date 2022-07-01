import datetime
from sre_parse import State
from django.db.models import Max
from django.shortcuts import render
from django.http import HttpResponse, request
from .models import StateHistory, ReportHIstory
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
# Create your views here.


def index(request):
    ups_qs = StateHistory.objects.raw('SELECT * FROM ups_monitor_statehistory group by ups_id HAVING date_add=max(date_add);')
    
    return render(request, 'ups_web/home.html', {'ups_qs': ups_qs})


def detail(request, id, slug):
    report_qs = ReportHIstory.objects.filter(ups=id).latest('date_add')
    state_qs = StateHistory.objects.filter(ups=id).latest('date_add')
    print(report_qs.model)
    return render(request, 'ups_web/detail.html', {
        'report_ups': report_qs,
        'ups': state_qs,
        'ip': state_qs.ups.ip,
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

# 
@api_view(['GET'])
def update_detail(request, ip):
    if request.method == 'GET':

        state_qs = ReportHIstory.objects.filter(ups__ip=ip).latest('date_add')
        serializer = ReportHistorySerializer(state_qs, context={'request': request})
        return Response({'data': serializer.data ,})


# Test, need delite
def orders_app(request):
    return render(request, 'ups_web/main_app.html')

def detail_ups(request):
    return render(request, "ups_web/detail_ups.html")

