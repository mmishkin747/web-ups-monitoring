from rest_framework import serializers
from .models import StateHistory, ReportHIstory


class StateHistorySerializer(serializers.ModelSerializer):

    date_add = serializers.DateTimeField(format="%B %d, %Y, %H:%M %P")

    class Meta:
        model = StateHistory
        fields = ('ups','main_voltage', 'temperature',
         'charge_battary', 'load','working_hours','date_add')


class ReportHistorySerializer(serializers.ModelSerializer):


    class Meta:
        model = ReportHIstory
        fields = ('model', 'voltage_battary', 'report_selftest', 'made_date', 'last_date_battary_replacement', 'serial_number', 'date_add')
