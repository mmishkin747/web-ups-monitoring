from datetime import datetime
from .telegram import send_telegram
datetime


def noti_main_voltage(ups, low_main_voltage, last_state, main_voltage,):
    if low_main_voltage:
        return noti_low_main_voltage(ups, main_voltage,)
    if last_state:
        return noti_report_main_voltage(ups, main_voltage)

def noti_low_main_voltage(ups, main_voltage):
    
    text = "low main voltage ups: {}, ip:{}, main voltage: {}".format(ups, ups.ip, main_voltage )
    status_code = send_telegram(text=text)
    return status_code

def noti_report_main_voltage(ups, main_volatge):
    
    text = "Status OK UPS: {}, ip:{}, main voltage: {}".format(ups, ups.ip, main_volatge)
    status_code = send_telegram(text=text)
    return status_code