from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

# Create your tests here.
class OrderTestCase(TestCase):
	fixtures = ['test.json']
	def setUp(self):
		self.client = Client()

	def test_user_api(self):
		response = self.client.get(reverse('gluttonyTw:user_api')+"?date=2017-02-01")
		self.assertEqual(response.status_code, 200)

	def test_join_order(self):
		payload={'今日特餐':2, 'period':'午餐'}
		response = self.client.post(reverse('gluttonyTw:join_order')+'?order_id=1', payload)
		self.assertEqual(response.status_code, 200)

	def test_join_order_list(self):
		response = self.client.get(reverse('gluttonyTw:join_order_list')+"?res_id=1")
		self.assertEqual(response.status_code, 200)

class RestTestCase(TestCase):
	fixtures = ['test.json']
	def setUp(self):
		self.client = Client()

	def test_rest_api(self):
		response = self.client.get(reverse('gluttonyTw:rest_api')+"?res_id=1")
		self.assertEqual(response.status_code, 200)

	def test_restaurant_prof(self):
		response = self.client.get(reverse('gluttonyTw:restaurant_prof')+"?res_id=1")
		self.assertEqual(response.status_code, 200)

	def test_restaurant_list(self):
		response = self.client.get(reverse('gluttonyTw:restaurant_list')+"?start=1")
		self.assertEqual(response.status_code, 200)

	def test_restaurant_menu(self):
		response = self.client.get(reverse('gluttonyTw:restaurant_menu')+"?res_id=1")
		self.assertEqual(response.status_code, 200)

	def test_restaurant_comment(self):
		response = self.client.get(reverse('gluttonyTw:restaurant_comment')+"?res_id=1&start=1")
		self.assertEqual(response.status_code, 200)