
from .models import UPS, StateHistory
from .state_ups.telnet_with_auth import get_state_ups
from .notification.telegram import post_telegram



def check():
    ups_list = UPS.objects.all()
    err_list =[]
    for ups in ups_list:
        try:
            state_ups = get_state_ups(host=ups.ip, port=ups.port, login=ups.login, password=ups.password)
            if state_ups.main_voltage < 10:
                post_telegram(text=f"{ups.name} {ups.ip} Main_voltage: {state_ups.main_voltage} ")
            print(f'{ups.name} - {state_ups}')
            StateHistory(ups=ups,
                        main_voltage=state_ups.main_voltage,
                        temperature=state_ups.temperature,
                        charge_battary=state_ups.charge_battery,
                        load=state_ups.load,
                        working_hours=state_ups.working_hours,

            ).save()
        except Exception as err:
            ups_err = f'ups = {ups} , ip = {ups.ip} , {err}'
            err_list.append(ups_err)
            

    if err_list:
        text = str()
        for i in range(len(err_list)):
            text += f'{i+1}. {err_list[i]} %2F'
    
    mess = f'We have some problems with:%2F {text}'
    print(mess)
    post_telegram(text=mess)
