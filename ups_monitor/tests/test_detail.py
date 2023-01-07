from django.test import TestCase
from threading import Thread
from .telnet_server import telnet_server_test
from ..models import UPS, ReportHIstory
import telnetlib
import logging
from logging import StreamHandler, Formatter
from ..state_ups.check import check_detail
import sys
from ..state_ups.error import ConnectError, ValueDetailError


logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)
handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)

class GetDatailTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(GetDatailTestCase, cls).setUpClass()
        th = Thread(target=telnet_server_test, args=(2066, 230, False))
        th.start()
        
    @classmethod
    def setUpTestData(cli):
        UPS.objects.get_or_create(
            name='testUPS',
            ip='127.0.0.1',
            port=2066,
            login = 'testlogin',
            password='12345',
            descript='ups for test',
            )
        ReportHIstory()
        
    @classmethod
    def tearDownClass(cls):
        telnet = telnetlib.Telnet(host='127.0.0.1', port=2066)
        telnet.write(b'close\r\n')
        telnet.close
        super().tearDownClass()

    def test_check_detail(self):
        logger.debug('Run check state')
        test_ups = UPS.objects.get(pk=1)
        detail_ups = check_detail(ups=test_ups)
        response = ReportHIstory.objects.get(ups=test_ups)
        self.assertEqual(detail_ups, response)


class ErrorDetailTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(ErrorDetailTestCase, cls).setUpClass()
        th = Thread(target=telnet_server_test, args=(2068, 230, False, True))
        th.start()
        
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
        ReportHIstory()
        
    @classmethod
    def tearDownClass(cls):
        telnet = telnetlib.Telnet(host='127.0.0.1', port=2068)
        telnet.write(b'close\r\n')
        telnet.close
        super().tearDownClass()


    def test_no_value_err_and_log(self):
        #This is try connect to server who no return value, test for writting log file
        logger.debug('Run test err detail, no value, con err and  check log')
        test_ups = UPS.objects.get(pk=1)
        with open("app.log", "r") as log_read:
            len_log_file_before = len(log_read.readlines())
        try:
            check_detail(ups=test_ups)
        except ValueDetailError:
            with open("app.log", "r") as log_read:
                len_log_file_after = len(log_read.readlines())
            self.assertEqual(len_log_file_before + 2, len_log_file_after)
        self.assertFalse


class ErrorConDetailTestCase(TestCase):
    @classmethod
    def setUpTestData(cli):
        UPS.objects.get_or_create(
            name='testUPS',
            ip='127.0.0.1',
            port=2069,
            login = 'testlogin',
            password='12345',
            descript='ups for test',
            )
        ReportHIstory()

    def test_con_err_and_log(self):
        #This is try connect to server who not response, test for writting log file
        logger.debug('Run test try detail, con err and  check log')
        test_ups = UPS.objects.get(pk=1)
        with open("app.log", "r") as log_read:
            len_log_file_before = len(log_read.readlines())
        try:
            check_detail(ups=test_ups)
        except ConnectError:
            with open("app.log", "r") as log_read:
                len_log_file_after = len(log_read.readlines())
            self.assertEqual(len_log_file_before + 1, len_log_file_after)
        self.assertFalse

