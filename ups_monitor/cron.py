
from .models import UPS, StateHistory
from .state_ups.check import check_state




def cron_check():
    ups_list = UPS.objects.all()
    for ups in ups_list:
        check_state(ups)



