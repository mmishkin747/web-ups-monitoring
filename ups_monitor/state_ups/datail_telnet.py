from datetime import datetime
import telnetlib
from collections import namedtuple
from enum import Enum
import logging
from .error import ConnectError, ValueDetailError



                
Detail_ups = namedtuple('detail',['model', 'voltage_battary', 'report_selftest',
                        'made_date', 'last_date_battary_replacement', 'serial_number',])


class Detail_Command_UPS(Enum):
    YES = b'Y'
    MODEL = b'\x01' # CTRL + A
    VOLTAGE_BATTARY = b'B'
    REPORT_SELFTEST = b'W'
    MADE_DATA = b'm'
    LAST_DATA_BATTARY_REPLACEMENT = b'x'
    SERIAL_NUMBER = b'n'


def get_detail_ups(login:str, password:str, host:str, port:int=2065):
    try:
        telnet = _connect_UPS(host=host, port=port)
        auth = _check_auth(telnet=telnet)
        if auth:
            telnet = _authenticate_connection(telnet=telnet, login=login, password=password)
    except Exception as err:
        err_text = f'Connect Error Host: {host} port: {port}, err: {err}'
        logging.error(err_text)
        raise ConnectError(err_text)
    try:
        values = _get_value_ups(telnet=telnet,  commands_ups=Detail_Command_UPS)
        values = _pars_values(values=values)
        state_ups = _valid_values(values=values)
    except Exception as err:
        err_text = f'Error get for param values for host: {host} port: {port}, err: {err}'
        logging.error(err_text)
        raise ValueDetailError(err_text)
    return state_ups


def _connect_UPS(host: str, port:int) -> telnetlib.Telnet:
    telnet = telnetlib.Telnet(host=host, port=port)
    return telnet

def _check_auth(telnet: telnetlib.Telnet) -> bool:
    if telnet.read_until(b'Username:', timeout=1):
        return True
    else:
        return False

def _get_value_ups(telnet:telnetlib.Telnet, commands_ups) -> dict:
    state_ups_dict = dict()
    for command in commands_ups:
        telnet.write(command.value)
        value = telnet.read_until(b'\n', timeout=4)
        if not value:
            err_text = f'No answer to command: {command.value} '
            logging.error(err_text)
            raise ValueDetailError(err_text)
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

def _valid_values(values: dict) -> Detail_ups:
        
    state_ups = Detail_ups(model=values.get('MODEL'),
                            voltage_battary=values.get('VOLTAGE_BATTARY'),
                            report_selftest=values.get('REPORT_SELFTEST'),
                            made_date=datetime.strptime(values.get('MADE_DATA'), '%m/%d/%y'),
                            last_date_battary_replacement=datetime.strptime(values.get('LAST_DATA_BATTARY_REPLACEMENT'), '%m/%d/%y'),
                            serial_number=values.get('SERIAL_NUMBER'),
    )

    return state_ups

