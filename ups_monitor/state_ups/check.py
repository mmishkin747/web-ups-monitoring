from ..models import StateHistory, ReportHIstory, ErrorUPS
from .state_telnet import get_state_ups
from .datail_telnet import get_detail_ups
from .notification.main_noti import noti_main_voltage
import logging



def check_state(ups):

    state_ups = get_state(ups)
    main_voltage = state_ups.main_voltage
    low_main_voltage = check_low_main_voltage(main_voltage=main_voltage)
    last_state = check_last_state(ups=ups)
    state = StateHistory.objects.create(
            ups=ups,
            main_voltage=state_ups.main_voltage,
            temperature=state_ups.temperature,
            charge_battary=state_ups.charge_battery,
            load=state_ups.load,
            working_hours=state_ups.working_hours,
            low_main_voltage = low_main_voltage,
        )

    if low_main_voltage + last_state == 1:
        noti_main_voltage(ups, low_main_voltage, last_state, main_voltage,)

    return state

def get_state(ups):
 
    state_ups = get_state_ups(host=ups.ip, port=ups.port, login=ups.login, password=ups.password)

    return state_ups

def check_low_main_voltage(main_voltage):
    if main_voltage < 190:
        return True
    return False

def check_last_state(ups) -> bool:
    try:
        last_state = StateHistory.objects.filter(ups=ups).latest('date_add')
    except Exception as err:
        logging.warning(f'No found StateHistory for ups: {ups}, err: {err}')
        return True

    return last_state.low_main_voltage



def check_detail(ups):

    detail_ups = get_detail_ups(host=ups.ip, port=ups.port, login=ups.login, password=ups.password)

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