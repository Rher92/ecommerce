from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status

from django.urls import reverse
from django.contrib.auth.models import User

from products.models import Product

class TestViews(APITestCase):

    def setUp(self):
        self.client = APIClient()
        user_password = 'Pepe.1234#'
        user = User.objects.create_user(
            username='john',
            email='john@email.com',
            password=user_password,
            is_active=True
        )
        url = reverse('token_obtain_pair')
        response = self.client.post(url, 
            {'username': user.username, 'password': user_password}
        )
        access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        
        self.product_name = 'manzana'
        self.product_price = 12.76
        self.product_stock = 34

        self.product = Product.objects.create(
            name=self.product_name,
            price=self.product_price,
            stock=self.product_stock
        )

    def test_delete_a_products(self):
        url = reverse('products:product-detail', args=[self.product.pk])
        response = self.client.delete(url)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(response.status_text, 'No Content')

    def test_update_a_specific_products(self):
        url = reverse('products:product-detail', args=[self.product.pk])
        data = {
            'name': 'mango',
            'price': 1.76,
            'stock': 133
        }
        response = self.client.put(url, data)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        response = response.json()
        self.assertEquals(response['name'], data['name'])
        self.assertEquals(response['price'], data['price'])
        self.assertEquals(response['stock'], data['stock'])
        
    def test_update_stock_a_specific_products(self):
        url = reverse('products:product-detail', args=[self.product.pk])
        data = {'stock': 12}
        response = self.client.patch(url, data)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        response = response.json()
        self.assertEquals(response['stock'], data['stock'])

    def test_retrieve_specific_products(self):
        url = reverse('products:product-detail', args=[self.product.pk])
        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        response = response.json()
        self.assertEquals(response['name'], self.product_name)
        self.assertEquals(response['price'], self.product_price)
        self.assertEquals(response['stock'], self.product_stock) 
        self.assertEquals(response['pk'], self.product.pk)

    def test_retrieve_all_products(self):
        url = reverse('products:product-list')
        response = self.client.get(url)
        lyst_response = response.json()

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(lyst_response, list)
        self.assertEquals(len(lyst_response), 1)
        self.assertEquals(lyst_response[0]['name'], self.product_name)
        self.assertEquals(lyst_response[0]['price'], self.product_price)
        self.assertEquals(lyst_response[0]['stock'], self.product_stock) 
        self.assertEquals(lyst_response[0]['pk'], self.product.pk)

    def test_create_product(self):
        url = reverse('products:product-list')
        data = {
            'name': 'manzana',
            'price': 12.76,
            'stock': 50
        }
        response = self.client.post(url, data=data)
        _response = response.json()

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(_response['name'], data['name'])
        self.assertEquals(_response['price'], data['price'])
        self.assertEquals(_response['stock'], data['stock'])
