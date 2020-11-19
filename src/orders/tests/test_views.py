from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status

from django.urls import reverse
from django.contrib.auth.models import User

from products.models import Product
from orders.models import Order, OrderDetail

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
        
        self.product = Product.objects.create(
            name='manzana',
            price=12.76,
            stock=34
        )

        self.order = Order.objects.create()

        self.order_detail = OrderDetail.objects.create(
            product=self.product,
            quantity=10,
            order=self.order
        )

    def test_create_order(self):
        url = reverse('orders:order-list')
        data = {
            'product': self.product.pk,
            'quantity': 20
        }
        response = self.client.post(url, data)
        order_data = response.json()

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(order_data['pk'], Order.objects.get(pk=order_data['pk']).pk)
        self.assertEquals(order_data['order_detail'], [])
        self.assertEquals(order_data['pesos_total'], 0)
        self.assertEquals(order_data['usd_total'], 0)
      
    def test_delete_order(self):
        url = reverse('orders:order-detail', args=[self.order_detail.order.pk])
        response = self.client.delete(url)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(response.status_text, 'No Content')

    def test_update_order(self):
        url = reverse('orders:order-detail', args=[self.order_detail.order.pk])
        data = {
            'product': self.order_detail.product.pk,
            'quantity': 5
        }        
        response = self.client.put(url, data)
        _response = response.json()

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(_response['pk'], self.order_detail.order.pk)
        self.assertEquals(_response['order_detail'][0]['quantity'], 5)
        self.assertEquals(_response['order_detail'][0]['product']['pk'], self.order_detail.product.pk)
        self.assertEquals(_response['usd_total'], self.order_detail.order.usd_total)
        self.assertEquals(_response['pesos_total'], self.order_detail.order.pesos_total)

    def test_add_product_to_order(self):
        product = Product.objects.create(
            name='pera',
            price=10.50,
            stock=600
        )    
        url = reverse('orders:order-detail', args=[self.order_detail.order.pk])
        data = {
            'product': product.pk,
            'quantity': 5
        }

        response = self.client.put(url, data)
        _response = response.json()

        for r in _response['order_detail']:
            if r['product']['pk']==product.pk:
                _order_detail = _response['order_detail'][0]

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(_response['pk'], self.order_detail.order.pk)
        self.assertEquals(_order_detail['quantity'], 5)
        self.assertEquals(_order_detail['product']['pk'], product.pk)
        self.assertEquals(_response['usd_total'], self.order_detail.order.usd_total)
        self.assertEquals(_response['pesos_total'], self.order_detail.order.pesos_total)

    def test_get_specific_order(self):
        url = reverse('orders:order-detail', args=[self.order_detail.order.pk])
        response = self.client.get(url)
        _response = response.json()

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(_response['pk'], self.order_detail.order.pk)
        self.assertEquals(_response['order_detail'][0]['quantity'], 10)
        self.assertEquals(_response['order_detail'][0]['product']['pk'], self.order_detail.product.pk)
        self.assertEquals(_response['usd_total'], self.order_detail.order.usd_total)
        self.assertEquals(_response['pesos_total'], self.order_detail.order.pesos_total)        