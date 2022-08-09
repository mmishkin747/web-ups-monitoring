
from enum import Enum
import logging
import telnetlib
import time
from collections import namedtuple
from enum import Enum
from .error import ConnectError, ValueStateError, NoneValueError



State_ups = namedtuple('state_ups', ['temperature', 'main_voltage',
                        'charge_battery', 'capasity_battery', 'working_hours', 'load'],)
                
logging.basicConfig(filename='app.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class State_Command_UPS(Enum):
    YES = b'Y'
    TEMPRETURE = b'C'
    MAINS_VOLTAGE = b'L'
    CHARGE_BATTERIES = b'f'
    CAPASITY_BATTERY = b'0'
    WORKING_HOURS = b'j'
    LOAD = b'P'




def get_state_ups( login:str, password:str, host:str, port:int=2065,) -> State_ups:
    try:
        telnet = _connect_UPS(host=host, port=port)
        auth = _check_auth(telnet=telnet)
        if auth:
            telnet = _authenticate_connection(telnet=telnet, login=login, password=password)
        values = _get_value_ups(telnet=telnet, command_ups=State_Command_UPS)
    except Exception as err:
        err_text = f'Connect Error Host: {host} port: {port}, err: {err}'
        logging.error(err_text)
        raise ConnectError(err_text)
    try:
        values = _pars_values(values=values)
        state_ups = _valid_values(values=values)
    except Exception as err:
        err_text = f'Error get or pars values for host: {host} port: {port}, err: {err}'
        logging.error(err_text)
        raise ValueStateError(err_text)
    return state_ups

def _connect_UPS(host: str, port:int) -> telnetlib.Telnet:
    telnet = telnetlib.Telnet(host=host, port=port)
    return telnet

def _check_auth(telnet: telnetlib.Telnet) -> bool:

    if telnet.read_until(b'Username:', timeout=1):
        return True
    else:
        return False

def _get_value_ups(telnet:telnetlib.Telnet, command_ups) -> dict:
    state_ups_dict = dict()
    for command in command_ups:
        telnet.write(command.value)
        value = telnet.read_until(b'\n', timeout=4)
        if not value:
            err_text = f'No answer to command: {command.value} '
            logging.error(err_text)
            raise NoneValueError(err_text)
        state_ups_dict[command.name] = value.decode('utf-8')
    telnet.close()
    return state_ups_dict
    
def _authenticate_connection(telnet: telnetlib.Telnet, login, password):
    login_b = bytes(login + "\n", encoding = "utf-8")
    password_b = bytes(password + '\n', encoding = "utf-8")
    telnet.write(login_b)
    telnet.read_until(b'Password:', timeout=4)
    telnet.write(password_b)
    telnet.read_until(b'\n', timeout=2)
    return telnet

def _pars_values(values: dict) -> dict:
    for key, value in values.items():
        values[key] = value.strip('\r\n').strip(':')
    return values

def _valid_values(values: dict) -> State_ups:


    try:
        capasity_battery=float(values.get('CAPASITY_BATTERY'))
    except ValueError:
        capasity_battery = -1
        
    state_ups = State_ups(temperature=float(values.get('TEMPRETURE')),
                            main_voltage=float(values.get('MAINS_VOLTAGE')),
                            charge_battery=float(values.get('CHARGE_BATTERIES')),
                            capasity_battery=capasity_battery,
                            working_hours=float(values.get('WORKING_HOURS')),
                            load=float(values.get('LOAD')),
    )


    return state_ups



if __name__=="__main__":
    print('Brest UPS')
    print(get_state_ups(host='10.55.10.100', port=2065, login='brest_monitoring', password=12345))