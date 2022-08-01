from django.shortcuts import get_object_or_404, redirect, render


from .models import Gprs, GprsCity

# Create your views here.


def gprs(request):
    return render(request, 'base.html')


def gprs_list(request, city_slug=None):
    clients = Gprs.objects.all()
    cities = GprsCity.objects.all()

    if city_slug:
        city=get_object_or_404(GprsCity, city=city_slug)
  
        clients = clients.filter(city=city)


    return render(request, 'gprs_list.html', {
        "clients": clients,
        "cities":cities,
        })


def client_datail(request, id):
    client = get_object_or_404(Gprs, id=id)

    return render(request, "gprs_detail.html", {"client": client})