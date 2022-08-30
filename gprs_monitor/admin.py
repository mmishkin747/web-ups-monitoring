from django.contrib import admin
from .models import GprsCity, Gprs

# Register your models here.

class GprsCityAdmin(admin.ModelAdmin):
    list_display = ['city','slug']

admin.site.register(GprsCity, GprsCityAdmin)


class GprsAdmin(admin.ModelAdmin):
    list_display = ['city', 'client', 'login_bft', 'password_bft', 'ppp',
                    'login_ftp', 'password_ftp', 'type_modem', 'imei_modem',
                    'operator_sim', 'number_sim', 'email_client', 'date_con', 'description']


admin.site.register(Gprs, GprsAdmin)