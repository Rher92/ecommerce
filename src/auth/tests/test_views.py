from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.urls.exceptions import NoReverseMatch

from rest_framework_simplejwt import views as jwt_views

from django.contrib.auth.models import User


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_password = 'Pepe.1234#'
        self.user = User.objects.create_user(
            username='john',
            email='john@email.com',
            password=self.user_password,
            is_active=True
        )    

    def test_get_token_obtain_par_and_token_refresh(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, 
            {'username': self.user.username, 'password': self.user_password}
        )

        self.assertEquals(response.status_code, 200)
        self.assertIsNotNone(response.json().get('refresh'))
        self.assertIsNotNone(response.json().get('access'))

        token_refresh = response.json().get('refresh')
        url = reverse('token_refresh')
        response = self.client.post(url, {'refresh': token_refresh})

        self.assertEquals(response.status_code, 200)
        self.assertIsNotNone(response.json().get('access')) 