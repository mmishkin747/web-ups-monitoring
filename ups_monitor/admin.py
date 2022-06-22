from django.contrib import admin
from .models import UPS, StateHistory, ReportHIstory
# Register your models here.




class UpsAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'ip', 'port', 'login', 'password', 'descript']
admin.site.register(UPS, UpsAdmin)

def name_ups(obj):
    return obj.ups.name

class StateHistoryAdmin(admin.ModelAdmin):
    list_display = [name_ups, 'main_voltage', 'temperature', 'charge_battary', 'load','working_hours','date_add']
    list_filter = ('ups__name', 'date_add')
admin.site.register(StateHistory, StateHistoryAdmin)


class ReportHistoryAdmin(admin.ModelAdmin):
    list_display = [name_ups, 'model', 'voltage_battary', 'report_selftest', 'made_date', 'last_date_battary_replacement', 'serial_number', 'date_add']
    list_filter = ('ups__name', 'date_add')
admin.site.register(ReportHIstory, ReportHistoryAdmin)