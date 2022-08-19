import sys
from django.test import TestCase
from .telnet_server import telnet_server_test
from ..state_ups.state_telnet import get_state_ups, State_ups
from ..state_ups.check import check_last_state, check_state
from ..models import UPS, StateHistory
from threading import Thread
from ..state_ups.error import ConnectError, ValueStateError
import logging
from logging import StreamHandler, Formatter
import telnetlib


logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)
handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)

class GetStateTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(GetStateTestCase, cls).setUpClass()
        th = Thread(target=telnet_server_test)
        th.start()
        
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
        StateHistory()
        
    @classmethod
    def tearDownClass(cls):
        telnet = telnetlib.Telnet(host='127.0.0.1', port=2065)
        telnet.write(b'close\r\n')
        telnet.close
        super().tearDownClass()

    def test_get_state(self):
        logger.debug('Run test get state')

        test_ups = UPS.objects.get(pk=1)

        result = get_state_ups(
            login=test_ups.login,
            password=test_ups.password,
            host=test_ups.ip,
            port=test_ups.port,
            )
        state_ups_test = State_ups(
            temperature=21.0,
            main_voltage=220.0,
            charge_battery=100,
            capasity_battery=99.0,
            working_hours=60.0,
            load=50,
        )
        self.assertEqual(result, state_ups_test)


    def test_check_state(self):
        logger.debug('Run check state')
        test_ups = UPS.objects.get(pk=1)
        result = check_state(test_ups)
        response = StateHistory.objects.get(ups=test_ups)
        self.assertEqual(result, response)


class ErrorStateTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(ErrorStateTestCase, cls).setUpClass()
        th = Thread(target=telnet_server_test, args=(2064, 230, False))
        th.start()

    @classmethod
    def setUpTestData(cli):
        UPS.objects.get_or_create(
            name='testUPS',
            ip='127.0.0.1',
            port=2064,
            login = 'testlogin',
            password='12345',
            descript='ups for test',
            )
        StateHistory()
    
    @classmethod
    def tearDownClass(cls):
        telnet = telnetlib.Telnet(host='127.0.0.1', port=2064)
        telnet.write(b'close\r\n')
        telnet.close
        super().tearDownClass()

    def test_check_with_no_valid_data(self):
        #this is try get no valid data, test for writing log file
        logger.debug('Run check with no valid data')
        with open("app.log", "r") as log_read:
                    len_log_file_before = len(log_read.readlines())
        test_ups = UPS.objects.get(pk=1)
        try:
            check_state(test_ups)
        except ValueStateError :
            with open("app.log", "r") as log_read:
                len_log_file_after = len(log_read.readlines())
            self.assertEqual(len_log_file_before + 1, len_log_file_after)

    def test_con_err_and_log(self):
        #This is try connect to server who not response, test for writting log file
        logger.debug('Run test try state con err and check log')
        test_ups = UPS.objects.get(pk=1)
        with open("app.log", "r") as log_read:
            len_log_file_before = len(log_read.readlines())
        try:
            check_state(ups=test_ups)
        except ConnectError:
            with open("app.log", "r") as log_read:
                len_log_file_after = len(log_read.readlines())
            self.assertEqual(len_log_file_before + 1, len_log_file_after)
        self.assertFalse

    def test_last_state(self):
        #Test last state low main valtage if obeject have not StateHistory, function shoud return True
        logger.debug('Run test last state')
        test_ups = UPS.objects.get(pk=1)
        result = check_last_state(test_ups)
        self.assertEqual(result, True)
                

class ErrorCoStateTestCase(TestCase):

    @classmethod
    def setUpTestData(cli):
        UPS.objects.get_or_create(
            name='testUPS',
            ip='127.0.0.1',
            port=2068,
            login = 'testlogin',
            password='12345',
            descript='ups for test',
            )
        StateHistory()

    def test_con_err_and_log(self):
        #This is try connect to server who not response, test for writting log file
        logger.debug('Run test try state con err and check log')
        test_ups = UPS.objects.get(pk=1)
        with open("app.log", "r") as log_read:
            len_log_file_before = len(log_read.readlines())
        try:
            check_state(ups=test_ups)
        except ConnectError:
            with open("app.log", "r") as log_read:
                len_log_file_after = len(log_read.readlines())
            self.assertEqual(len_log_file_before + 1, len_log_file_after)
        self.assertFalse

class RealUpsTestCase(TestCase):

    # def test_real_ups(self):
    #     result = get_state_ups(login="brest_monitoring", password='12345', host='10.55.100.18' )
    #     print('-------------------Test real ups-----------------------')
    #     print(result)
    pass
