
from pandas import DataFrame, read_csv
from datetime import datetime


#import matplotlib.pyplot as plt

import pandas as pd

from .models import GprsCity, Gprs
from typing import NamedTuple

file = r'gprs_monitor/ERIP-GPRS.xls'
file1 = r'ERIP-GPRS.xls'
df = pd.read_excel(file)


def unic_city():
    list_gprs_city = []
    for city in df['Город']:
        if city in list_gprs_city:
            continue
        else:
            list_gprs_city.append(city)

    return list_gprs_city

def creat_db_city(list_city = unic_city()):
    for city in list_city:
        GprsCity(city=city).save()

class GprsClient(NamedTuple):
    city: str
    client: str | None
    login_bft: str | None
    password_bft: str | None
    ppp: str | None
    login_ftp: str | None
    password_ftp: str | None
    type_modem: str | None
    imei_modem: str | None
    operator_sim: str | None
    number_sim: str | None
    email_client: str | None
    date_con: str | None
    description: str | None


def get_client_list():
    gprs_client_list = []
    for index, row in df.iterrows():
        #print(row.keys())
        #print(f'City: {row.get("Город")} {row.get("Договор № ")}')
        client = GprsClient(
            city=row.get('Город'),
            client=row.get('Клиент ЕРИП GPRS'),
            login_bft=row.get('Login BFN'),
            password_bft=row.get('Password BFN'),
            ppp=row.get('PPP:'),
            login_ftp = row.get('Login FTP'),
            password_ftp = row.get('Password FTP'),
            type_modem=row.get('Тип модема'),
            imei_modem=row.get('IMEI'),
            operator_sim=row.get('SIM'),
            number_sim=row.get('№ SIM'),
            email_client=row.get('e-mail клиента'),
            date_con=row.get('Дата тест. подкл-я'),
            description=row.get('Пометки'),
        )
        gprs_client_list.append(client)

    return gprs_client_list

def pars_date(date):
    print(str(date))
    if date:
        valid_date = datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"),
        return valid_date

" %d.%m.%Y"

def create_db_gprs(list_client=get_client_list()):

    for client_gprs in list_client:
        client_gprs.city
        Gprs(
            city=GprsCity.objects.get(city=client_gprs.city),
            client=client_gprs.client,
            login_bft=client_gprs.login_bft,
            password_bft=client_gprs.password_bft,
            ppp=client_gprs.ppp,
            login_ftp=client_gprs.login_ftp,
            password_ftp=client_gprs.password_ftp,
            type_modem=client_gprs.type_modem,
            imei_modem=client_gprs.imei_modem,
            operator_sim=client_gprs.operator_sim,
            number_sim=client_gprs.number_sim,
            email_client=client_gprs.email_client,
            date_con= client_gprs.date_con,
            description=client_gprs.description,
        ).save()


['Город', 'Договор №', 'УНП', 'Клиент ЕРИП GPRS', 'Login BFN',
       'Password BFN', 'PPP:', 'Login FTP', 'Password FTP', 'Тип модема',
       'IMEI', 'SIM', '№ SIM', 'PIN SIM', 'e-mail клиента',
       'Дата тест. подкл-я', 'Пометки', 'Unnamed: 17'],

