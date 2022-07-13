from datetime import datetime
import telnetlib
import time
from collections import namedtuple
from enum import Enum



                
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
    telnet = _connect_UPS(host=host, port=port)
    auth = _check_auth(telnet=telnet)
    if auth:
        telnet = _authenticate_connection(telnet=telnet, login=login, password=password)
   
    values = _get_value_ups(telnet=telnet)
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

def _get_value_ups(telnet:telnetlib.Telnet) -> dict:
    state_ups_dict = dict()
    for command in Detail_Command_UPS:
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

def _valid_values(values: dict) -> Detail_ups:
    '''
    for key, value in values.items():
        try:
            values[key] = float(value)
        except ValueError:
            values[key] = 0
    '''

    
    state_ups = Detail_ups(model=values.get('MODEL'),
                            voltage_battary=values.get('VOLTAGE_BATTARY'),
                            report_selftest=values.get('REPORT_SELFTEST'),
                            made_date=datetime.strptime(values.get('MADE_DATA'), '%m/%d/%y'),
                            last_date_battary_replacement=datetime.strptime(values.get('LAST_DATA_BATTARY_REPLACEMENT'), '%m/%d/%y'),
                            serial_number=values.get('SERIAL_NUMBER'),
    )

    return state_ups



if __name__=="__main__":
    print('Brest UPS')
    print(get_detail_ups(host='10.55.10.100', port=2065, login='brest_monitoring', password=12345))