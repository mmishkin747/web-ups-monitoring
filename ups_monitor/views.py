from datetime import timedelta
from django.shortcuts import redirect, render
from .models import UPS, StateHistory, ReportHIstory
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .serializers import *
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .state_ups.check import check_state, check_detail
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


def index(request):

    return redirect('/ups')

@login_required
def ups_list(request):
    try:
        ups_qs = StateHistory.objects.raw('SELECT * FROM ups_monitor_statehistory group by ups_id HAVING date_add=max(date_add);')
    except Exception:
        pass
    return render(request, 'ups_list.html', {'ups_qs': ups_qs, })
                                               
@login_required
def detail(request, ip):
    ups = get_object_or_404(UPS, ip=ip)
    try:
        report_qs = ReportHIstory.objects.filter(ups=ups).latest('date_add')
    except Exception:
        report_qs = ReportHIstory.objects.create(ups=ups)

    state_qs = StateHistory.objects.filter(ups__ip=ip).latest('date_add')

    return render(request, 'detail.html', {
        'report_ups': report_qs,
        'ups': state_qs,
        'ip': state_qs.ups.ip,
        'buttom': request.user.has_perm('ups_monitor.add_post')
    })

class UpsStateList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        ups_qs = StateHistory.objects.raw('SELECT * FROM ups_monitor_statehistory group by ups_id HAVING date_add=max(date_add);')
        serializer = StateHistorySerializer(ups_qs, context={'request': request}, many=True)
        return Response({'data': serializer.data })


class CheckStateNow(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, ip):
        ups = UPS.objects.get(ip=ip)
        try:
            state_qs = StateHistory.objects.filter(ups__ip=ip).latest('date_add')
            
        except Exception:
            state = check_state(ups)
            serializer = StateHistorySerializer(state, context={'request': request})
            return Response({'data': serializer.data,})
        last_state = state_qs.date_add + timedelta(minutes=1)
        if last_state < timezone.now():
            state = check_state(ups)      
        else:
            state = state_qs
        serializer = StateHistorySerializer(state, context={'request': request})
        return Response({'data': serializer.data,})
        

class UpdateDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, ip):
        if not request.user.has_perm('ups_monitor.add_post'):
            print(f"------ {request.user.has_perm('ups_monitor.add_post')}")
            raise PermissionDenied
        if  request.method == 'GET':
            ups = UPS.objects.get(ip=ip)
            detail = check_detail(ups)
            print(detail)
            serializer = ReportHistorySerializer(detail, context={'request': request})
            return Response({'data': serializer.data ,})


#--------------------------------------------------------------------------------------------------------------------------

#  future
# @login_required   
# @api_view(['GET'])
# def ups_detail(request, ip):
#     if request.method == 'GET':
#         state_qs = ReportHIstory.objects.filter(ups__ip=ip).latest('date_add')
#         serializer = ReportHistorySerializer(state_qs, context={'request': request})
#         return Response({'data': serializer.data ,})


# @api_view(['GET'])
# def ups_state_list(request):
#     if request.method == 'GET':
#         ups_qs = StateHistory.objects.raw('SELECT * FROM ups_monitor_statehistory group by ups_id HAVING date_add=max(date_add);')
#         serializer = StateHistorySerializer(ups_qs, context={'request': request}, many=True)
#         return Response({'data': serializer.data })

# @login_required
# @api_view(['GET'])
# def check_state_now(request, ip):
#     ups = UPS.objects.get(ip=ip)
#     try:
#         state_qs = StateHistory.objects.filter(ups__ip=ip).latest('date_add')
        
#     except Exception:
#         state = check_state(ups)
#         serializer = StateHistorySerializer(state, context={'request': request})
#         return Response({'data': serializer.data,})
#     last_state = state_qs.date_add + timedelta(minutes=1)
#     if last_state < timezone.now():
#         state = check_state(ups)      
#     else:
#         state = state_qs
#     serializer = StateHistorySerializer(state, context={'request': request})
#     return Response({'data': serializer.data,})

# @login_required
# @api_view(['GET'])
# def update_detail(request, ip):
#     if not request.user.has_perm('ups_monitor.add_post'):
#         print(f"------ {request.user.has_perm('ups_monitor.add_post')}")
#         raise PermissionDenied
#     if  request.method == 'GET':
#         ups = UPS.objects.get(ip=ip)
#         detail = check_detail(ups)
#         print(detail)
#         serializer = ReportHistorySerializer(detail, context={'request': request})
#         return Response({'data': serializer.data ,})