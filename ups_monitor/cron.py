
from .models import UPS, StateHistory
from .state_ups.telnet_with_auth import get_state_ups




def check():
    ups_list = UPS.objects.all()
    for ups in ups_list:
        state_ups = get_state_ups(host=ups.ip)
        print(f'{ups.name} - {state_ups}')
        StateHistory(ups=ups,
                    main_voltage=state_ups.main_voltage,
                    temperature=state_ups.temperature,
                    charge_battary=state_ups.charge_battery,
                    load=state_ups.load,
                    working_hours=state_ups.working_hours,

        ).save()
