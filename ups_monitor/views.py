import datetime
from sre_parse import State
from django.db.models import Max
from django.shortcuts import render
from django.http import HttpResponse, request
from .models import StateHistory, ReportHIstory
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
    })