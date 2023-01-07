from django.contrib.auth.models import User
from django.test import TestCase
from ..models import UPS


class AuthTestCase(TestCase):
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
        User.objects.create(username='testuser', password='12345')
    
    def test_redir_ups(self):
        response = self.client.get('/ups/')
        self.assertEqual(response.status_code, 302)
        
    def test_redir_detail_ups(self):
        ups = UPS.objects.get(pk=1)
        response = self.client.get('/'+ ups.ip +'/')
        self.assertRedirects(response, f'/login/?next=%2F{ups.ip}%2F')

    def test_page_login(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_auth(self):
        user = User.objects.get(pk=1)
        response = self.client.post('/login/', {'name':user.username, 'passwd': user.password})       
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = self.client.get('/ups/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)


 

