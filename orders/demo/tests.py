from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Order, OrderDetail, Product
from .serializers import OrderSerializer, ProductSerializer
import json, datetime, random

NAMES = ["puerta", "vaso", "cuchara", "plato"]
PRICES = [5.50 ,10 ,25 ,30 ,100, 200.98, 300.76]

class OrderViewSetTestCase(APITestCase):

    def setUp(self):
        '''
        Initialize test data.
        Orders will have randoms products and quantities
        '''
        self.orders = [Order.objects.create(date_time=datetime.datetime.now()) for a in range(3)]
        self.products = [Product.objects.create(price=random.choice(PRICES), name=NAMES[a]) for a in range(4)]
        for order in self.orders:
            for r in range(random.randint(1,3)):
                OrderDetail.objects.create(order=order, cuantity=random.randint(1,10), product=self.products[r])
        self.credentials = {'username':'user', 'password':'password'}
        user = User.objects.create(**self.credentials)
        user.is_active = True
        user.save()
        self.user_test = user

    def test_order_list(self):
        '''
        Check orders list endpoint
        '''
        self.client.force_authenticate(user=self.user_test)
        response = self.client.get('/orders/')
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(len(self.orders), len(response.data))

        for order in self.orders:
            self.assertIn(OrderSerializer(instance=order).data, response.data)

    def test_order_specific(self):
        '''
        Check first order view
        '''
        self.client.force_authenticate(user=self.user_test)
        response = self.client.get('/orders/1/')
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(OrderSerializer(instance=self.orders[0]).data, response.data)

    def test_create_order(self):
        '''
        Check order create endpoint. Fail cases included.
        '''
        self.client.force_authenticate(user=self.user_test)
        data = {
                    "date_time": "2075-10-24T15:31:30",
                    "details": [
                        {
                            "cuantity": 3,
                            "product": 1
                        },
                        {
                            "cuantity": 1,
                            "product": 2
                        }
                    ]
                }

        response = self.client.post('/orders/', data, format='json')
        new_order = Order.objects.get(date_time=data["date_time"])
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertEquals(OrderSerializer( instance=new_order).data, response.data)             #check endpoint response

        wrong_data = {
                    "date_time": "2085-10-24T15:31:30",
                    "details": [
                        {
                            "cuantity": 0,    #wrong value
                            "product": 1
                        }
                    ]
                }
        response = self.client.post('/orders/', wrong_data, format='json')
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

        wrong_data2 = {
                    "date_time": "2085-10-24T15:31:30",
                    "details": [
                        {
                            "cuantity": 1,
                            "product": 1
                        },
                        {
                            "cuantity": 1,
                            "product": 1        #repeated product
                        }
                    ]
                }
        response = self.client.post('/orders/', wrong_data2, format='json')
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)



    def test_modify_order(self):
        '''
        Check update and patch actions
        '''
        self.client.force_authenticate(user=self.user_test)
        order = Order.objects.create(date_time=datetime.datetime.now())
        product = Product.objects.create(name="modify_me", price=10)
        orders_detail = OrderDetail.objects.create(cuantity=1, product=product, order=order)

        data_put = {
                    "date_time":"2025-10-24T15:31:30",       #this changed
                    "details":[
                                    {
                                    "cuantity":2,            #this changed
                                    "product": product.id
                                    }
                               ]
                }
        response = self.client.put('/orders/{}/'.format(order.id), data_put, format='json')
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(data_put['details'][0]['cuantity'], response.data['details'][0]['cuantity'])
        self.assertEquals(data_put['date_time'],response.data['date_time'])

        data_patch = {
                     "details":[
                                    {
                                    "cuantity":10,        #partial update
                                    "product": product.id
                                    }
                                ]
                    }
        response = self.client.patch('/orders/{}/'.format(order.id), data_patch, format='json')
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(data_patch['details'][0]['cuantity'], response.data['details'][0]['cuantity'])

    def test_delete_order(self):
        '''
        Check order deletion
        '''
        order = Order.objects.create(date_time=datetime.datetime.now())
        order_deleted_pk = order.pk
        self.client.force_authenticate(user=self.user_test)
        response = self.client.delete('/orders/{}/'.format(order.pk))
        self.assertEquals(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(Order.objects.filter(pk=order_deleted_pk))


class ProductViewSetTestCase(APITestCase):

    def setUp(self):
        '''
        Initialize test data.
        Products will have randoms prices
        '''
        self.products = [Product.objects.create(price=random.choice(PRICES), name=NAMES[a]) for a in range(4)]
        self.credentials = {'username':'user', 'password':'password'}
        user = User.objects.create(**self.credentials)
        user.is_active = True
        user.save()
        self.user_test = user

    def test_product_list(self):
        '''
        Check orders list endpoint
        '''
        self.client.force_authenticate(user=self.user_test)
        response = self.client.get('/products/')
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(len(self.products), len(response.data))

        for product in self.products:
            self.assertIn(ProductSerializer(instance=product).data, response.data)

    def test_product_specific(self):
        '''
        Check first product view
        '''
        self.client.force_authenticate(user=self.user_test)
        response = self.client.get('/products/1/')
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(ProductSerializer(instance=self.products[0]).data, response.data)

    def test_create_product(self):
        '''
        Check product create endpoint
        '''
        self.client.force_authenticate(user=self.user_test)
        data = { "name": "zapatillas", "price": 100 }

        response = self.client.post('/products/', data, format='json')
        new_product = Product.objects.get(name=data["name"])
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertEquals(ProductSerializer( instance=new_product).data, response.data)             #check endpoint response

    def test_modify_product(self):
        '''
        Check update and patch actions
        '''
        self.client.force_authenticate(user=self.user_test)
        product = Product.objects.create(name="modify_me", price=10)

        data_put = { "name":"new_name", "price": 20 }

        response = self.client.put('/products/{}/'.format(product.id), data_put, format='json')
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(data_put['name'], response.data['name'])
        self.assertEquals(data_put['price'],response.data['price'])

        data_patch = { "price": 70 }  #partial update

        response = self.client.patch('/products/{}/'.format(product.id), data_patch, format='json')
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(data_patch['price'], response.data['price'])


    def test_delete_product(self):
        '''
        Check product deletion
        '''
        product = Product.objects.create(name="delete_me", price=10)
        product_deleted_pk = product.pk
        self.client.force_authenticate(user=self.user_test)
        response = self.client.delete('/products/{}/'.format(product.pk))
        self.assertEquals(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(Product.objects.filter(pk=product_deleted_pk))
