from django.shortcuts import redirect, render

# Create your views here.


def gprs(request):
    return render(request, 'base.html')