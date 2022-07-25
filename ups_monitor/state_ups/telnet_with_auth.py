
from enum import Enum

import telnetlib
import time
from collections import namedtuple
from enum import Enum


USERNAME = b'brest_monitoring\n'
PASSWORD = b'12345\n'

State_ups = namedtuple('state_ups', ['temperature', 'main_voltage',
                        'charge_battery', 'capasity_battery', 'working_hours', 'load'],)
                


class State_Command_UPS(Enum):
    YES = b'Y'
    TEMPRETURE = b'C'
    MAINS_VOLTAGE = b'L'
    CHARGE_BATTERIES = b'f'
    CAPASITY_BATTERY = b'0'
    WORKING_HOURS = b'j'
    LOAD = b'P'



def get_state_ups( login, password, host:str, port:int=2065,):
    telnet = _connect_UPS(host=host, port=port)
    auth = _check_auth(telnet=telnet)
    if auth:
        telnet = _authenticate_connection(telnet=telnet, login=login, password=password)

    values = _get_value_ups(telnet=telnet, command_ups=State_Command_UPS)
    values = _pars_values(values=values)
    state_ups = _valid_values(values=values)
    return state_ups

def _connect_UPS(host: str, port:int) -> telnetlib.Telnet:
    telnet = telnetlib.Telnet(host=host, port=port)
    return telnet

def _check_auth(telnet: telnetlib.Telnet) -> bool:
    time.sleep(1)
    if telnet.read_very_eager().decode('utf-8'):
        return True
    else:
        return False

def _get_value_ups(telnet:telnetlib.Telnet, command_ups) -> dict:
    state_ups_dict = dict()
    for command in command_ups:
        telnet.write(command.value)
        time.sleep(1)
        value = telnet.read_very_eager()
        state_ups_dict[command.name] = value.decode('utf-8')
    return state_ups_dict
    
def _authenticate_connection(telnet: telnetlib.Telnet, login, password):
    login_b = bytes(login + "\n", encoding = "utf-8")
    password_b = bytes(password + '\n', encoding = "utf-8")
    telnet.write(login_b)
    time.sleep(1)
    telnet.read_until(b'Password:')
    telnet.write(password_b)
    return telnet

def _pars_values(values: dict) -> dict:
    for key, value in values.items():
        values[key] = value.strip('\r\n').strip(':')
    values.pop('YES', None)
    return values

def _valid_values(values: dict) -> State_ups:
    for key, value in values.items():
        try:
            values[key] = float(value)
        except ValueError:
            values[key] = 0

    state_ups = State_ups(temperature=values.get('TEMPRETURE'),
                            main_voltage=values.get('MAINS_VOLTAGE'),
                            charge_battery=values.get('CHARGE_BATTERIES'),
                            capasity_battery=values.get('CAPASITY_BATTERY'),
                            working_hours=values.get('WORKING_HOURS'),
                            load=values.get('LOAD'),
    )

    return state_ups



if __name__=="__main__":
    print('Brest UPS')
    print(get_state_ups(host='10.55.10.100', port=2065, login='brest_monitoring', password=12345))