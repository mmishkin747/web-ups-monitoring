from django.test import TestCase
from ..state_ups.notification.telegram import send_telegram
from ..state_ups.notification.main_noti import noti_low_main_voltage, noti_report_main_voltage
from ..models import UPS


class TelegramTest(TestCase):
    @classmethod
    def setUpTestData(cli):
        UPS.objects.get_or_create(
            name='testUPS',
            ip='127.0.0.1',
            port=2065,
            login = 'testlogin',
            password='12345',
            descript='ups for test',
            )

    def test_send_telegram(self):
        text = "Test message telegram"
        response = send_telegram(text = text)
        self.assertEqual(response, 200)

    def test_noti_low_main_voltage(self):
        ups = UPS.objects.get(pk=1)
        response_noti = noti_low_main_voltage(ups=ups, main_voltage=0)
        self.assertEqual(response_noti, 200)

    def test_noti_report_main_voltage(self):
        ups = UPS.objects.get(pk=1)
        response_noti = noti_report_main_voltage(ups=ups, main_volatge=220)
        self.assertEqual(response_noti, 200)



        