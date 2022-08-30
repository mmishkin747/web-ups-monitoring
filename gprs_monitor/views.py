from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required 

from .models import Gprs, GprsCity

# Create your views here.


def gprs(request):
    return render(request, 'base.html')

@login_required
def gprs_list(request, slug=None):
    clients = Gprs.objects.all()
    cities = GprsCity.objects.all()

    if slug:
        city=get_object_or_404(GprsCity, slug=slug,)
  
        clients = clients.filter(city=city)


    return render(request, 'gprs_list.html', {
        "clients": clients,
        "cities":cities,
        })

@login_required
def client_datail(request, id):
    client = get_object_or_404(Gprs, id=id)

    return render(request, "gprs_detail.html", {"client": client})