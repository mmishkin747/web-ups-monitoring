from ..models import StateHistory, ReportHIstory
from .telnet_with_auth import get_state_ups
from .datail_telnet import get_detail_ups


def check_state(ups):
    try:
        state_ups = get_state_ups(host=ups.ip, port=ups.port, login=ups.login, password=ups.password)
        print(state_ups)
    except Exception as err:
            ups_err = f'ups = {ups} , ip = {ups.ip} , {err}'
            return None


    state = StateHistory.objects.create(
            ups=ups,
            main_voltage=state_ups.main_voltage,
            temperature=state_ups.temperature,
            charge_battary=state_ups.charge_battery,
            load=state_ups.load,
            working_hours=state_ups.working_hours,
        )

    return state


def check_detail(ups):
    try:
        detail_ups = get_detail_ups(host=ups.ip, port=ups.port, login=ups.login, password=ups.password)
    except Exception as err:
        return None
    
    detail = ReportHIstory.objects.create(
            ups=ups,
            model = detail_ups.model,
            voltage_battary = detail_ups.voltage_battary,
            report_selftest = detail_ups.report_selftest,
            made_date = detail_ups.made_date,
            last_date_battary_replacement = detail_ups.last_date_battary_replacement,
            serial_number = detail_ups.serial_number,
        )
    return detail
    


def low_main_voltage(ups, main_voltage):
    pass

def write_log():
    pass