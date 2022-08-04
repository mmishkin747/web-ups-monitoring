
from django.test import TestCase
from .telnet_server import telnet_server_test
from ..state_ups.state_telnet import get_state_ups
from ..models import UPS
from threading import Thread


class GetStateTestCase(TestCase):

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


    def test_get_state(self):
        th = Thread(target=telnet_server_test)
        th.start()
        test_ups = UPS.objects.get(pk=1)

        result = get_state_ups(
            login=test_ups.login,
            password=test_ups.password,
            host=test_ups.ip,
            port=test_ups.port,
            )
        print(result)
        
