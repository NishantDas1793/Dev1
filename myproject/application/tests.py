from rest_framework.test import APITestCase, URLPatternsTestCase
from django.urls import include, path, reverse
from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from django.urls import resolve
from .views import home, main
from .models import People, Address
import logging
from django.test.client import MULTIPART_CONTENT, BOUNDARY, encode_multipart
from .serializers import peopleSerializers, AddressSerializers
import json
# from .views import main
from unittest import TestCase as TC
from unittest.mock import patch, Mock
from application import views, models
import threading
# Create your tests here.

# import IPython; IPython.embed();

logging.basicConfig(filename='test.log',level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

class HomeTests(TestCase):
	def test_home_view_status_code(self):
		url = reverse('home')
		response = self.client.get(url)
		self.assertEquals(response.status_code,200)

	# def test_main(self):
	# 	answer = self.main()


# to check if django returned correct view function
	# def test_home_view_resolve(self):
	# 	view = resolve('application/')
	# 	self.assertEquals(view.func, home)

class PeopleListTests(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.address_data = Address.objects.create(street='123 abc',
			city='abcity',
			State='abcstate',
			Zip_code = ''
			)
		self.people = People.objects.create(Name='Rahul', 
			age='21', 
			email='rahul@gmail.com', 
			sex='M', 
			height='6', 
			weight='72', 
			relationship='OR', 
			address=self.address_data
			)
		# self.serializer = peopleSerializers(instance = self.people)
		url = reverse('list')
		self.response = self.client.get(url)

	def test_people_view_status_code(self):
		self.assertEquals(self.response.status_code,200)

	def test_single_address(self):
		address_count = Address.objects.count()
		self.assertEquals(address_count, 1)

	def test_single_people(self):
		people_count = People.objects.count()
		self.assertEquals(people_count,1)

	def test_create_data(self):
		url = reverse('post')
		data = {"Name":"hdj","age":43,"email":"gsgs@gshsh.cgc",
		"sex":"M","height":6,"weight":345,"relationship":"U",
		"address":{"street":"ghdh","city":"odik","State":"rsgs","Zip_code":""}}
		# import IPython; IPython.embed();
		response = self.client.post(url, data, format='json')
		self.assertEquals(response.json()['message'], 'People Created')
		# self.assertEquals(response.json['message'], 'People Created')
		# serializer = peopleSerializers(data = data)
		# self.assertTrue(serializer.is_valid())
		# self.assertTrue(serializer.save())
		self.assertEquals(response.status_code, 200)
		person = People.objects.filter(Name='hdj').first()
		self.assertEquals(person.age, 43)

	def test_create_invalid_data(self):
		url = reverse('post')
		data = {"Name":"hdj","age":43,"email":"",
		"sex":"M","height":6,"weight":345,"relationship":"U",
		"address":{"street":"ghdh","city":"odik","State":"rsgs","Zip_code":""}}
		# import IPython; IPython.embed();
		response = self.client.post(url, data, format='json')
		# self.assertEquals(response.json()['message'], 'People Created')
		# serializer = peopleSerializers(data = data)
		# self.assertTrue(serializer.is_valid())
		# self.assertTrue(serializer.save())
		self.assertEquals(response.status_code, 400)
		person = People.objects.filter(Name='hdj').first()
		# self.assertEquals(person.age, 43)
		

	def test_check_serializer_valid(self):
		data = {"Name":"hdj","age":43,"email":"gsgs@gshsh.cgc",
		"sex":"M","height":6,"weight":345,"relationship":"U",
		"address":{"street":"ghdh","city":"odik","State":"rsgs","Zip_code":""}}
		serializer = peopleSerializers(data = data)
		if serializer.is_valid(raise_exception=True):
			# return serializer.data
			self.assertEquals(serializer.data, data)
			self.assertEquals(serializer.is_valid(raise_exception=True), True)
		return serializer.errors
		# self.assertTrue(serializer.is_valid())
		# self.assertTrue(serializer.save())

	def test_list_people(self):
		url = reverse('people_list')
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)

	def test_list_people_detail(self):
		url = reverse('people_detail', kwargs={'pk': self.people.pk})
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)

	def test_list_people_update(self):
		url = reverse('people_update', kwargs={'pk': self.people.pk})
		data = {"Name":"hdj","age":43,"email":"gsgs@gshsh.cgc",
		"sex":"M","height":6,"weight":345,"relationship":"U",
		"address":{"street":"ghdh","city":"odik","State":"rsgs","Zip_code":""}}
		response = self.client.put(url, data, format='json')
		self.assertEquals(response.status_code, 200)

	def test_list_people_invalid_update(self):
		url = reverse('people_update', kwargs={'pk': self.people.pk})
		data = {"Name":"hsshdh","age":43,"email":"gsgs@gshsh.cgc",
		"sex":"M","height":6,"weight":345,"relationship":"U",
		"address":{"street":"ghdh","city":"","State":"rsgs","Zip_code":""}}
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)

	def test_list_people_invalid_updatel(self):
		url = reverse('people_update', kwargs={'pk': self.people.pk})
		data = {}
		response = self.client.put(url, data, format='json')
		self.assertEquals(response.status_code, 200)	



	def test_list_people_delete(self):
		url = reverse('people_delete', kwargs={'pk': self.people.pk})
		self.client.delete(url)
		people_count = People.objects.count()
		self.assertEquals(people_count,0)

		


class peopleSerializers_test(TestCase):


	def test_valid_address_serializer(self):
		data = {"street":"ghdh","city":"odik","State":"rsgs","Zip_code":""}
		serializer = AddressSerializers(data = data)
		self.assertEquals(serializer.is_valid(), True)

	def test_invalid_address_serializer(self):
		data = {"street":"","city":"","State":"","Zip_code":""}
		serializer = AddressSerializers(data = data)
		self.assertEquals(serializer.is_valid(), False)

	def test_valid_people_serializer(self):
		data = {"Name":"hdj","age":43,"email":"gsgs@gshsh.cgc",
		"sex":"M","height":6,"weight":345,"relationship":"U",
		"address":{"street":"ghdh","city":"odik","State":"rsgs","Zip_code":""}}
		serializer = peopleSerializers(data = data)
		self.assertEquals(serializer.is_valid(), True)

	def test_invalid_people_serializer(self):
		data = {"Name":"","age":43,"email":"gsgs@gshsh.cgc",
		"sex":"M","height":6,"weight":345,"relationship":"U",
		"address":{"street":"ghdh","city":"odik","State":"rsgs","Zip_code":""}}
		serializer = peopleSerializers(data = data)
		self.assertEquals(serializer.is_valid(), False)

	def test_update_people_serializer(self):
		data = {"Name":"","age":43,"email":"gsgs@gshsh.cgc",
		"sex":"M","height":6,"weight":345,"relationship":"U",
		"address":{"street":"ghdh","city":"odik","State":"rsgs","Zip_code":""}}
		serializer = peopleSerializers(data = data)
		if serializer.is_valid():
			address = serializer.validated_data.get('address')
			self.assertEquals(address, {"street":"ghdh","city":"odik","State":"rsgs","Zip_code":""})
		

class xyzTestcase(APITestCase, URLPatternsTestCase):
	urlpatterns = [
    path('application/', include('application.urls')),

	]

	def setUp(self):
		# self.client = APIClient()
		self.address_data = Address.objects.create(street='123 abc',
			city='abcity',
			State='abcstate',
			Zip_code = ''
			)
		self.people = People.objects.create(Name='Rahul', 
			age='21', 
			email='rahul@gmail.com', 
			sex='M', 
			height='6', 
			weight='72', 
			relationship='OR', 
			address=self.address_data
			)

	def test_query_data(self):
		url = '/application/'#'application/?q=a'
		# response = self.client.get(url)
		# self.assertEquals(response.status_code, 200)
		# self.assertEqual(len(response.data), 1)
		# self.assertEqual(json.loads(response.content), {'id': 1, 'Name': 'Rahul'})	
		# return People.objects.first()
		response = self.client.get("/application/", {'q': self.people.Name})
		self.assertEquals(response.status_code, 200)


def mock_print_cube(num): 
    print("Cube: {}".format(num * num * num)) 
  
def mock_print_square(num): 
    print("Square: {}".format(num * num)) 

def mock_male():
	xyz = [
	{
                'id': 1,
                'Name': 'abc',
                'age': 23,
                'email':'abc@gmail.com',
                'sex': 'M',
                'height': 6,
                'weight' : 60,
                'relationship': 'OR',
                'address':{"street":"ghdh","city":"odik","State":"rsgs","Zip_code":""}
    }
	]
	return xyz

# def mock_start(x, n):
# 	if x=='s':
# 		return mock_print_square(n)
# 	elif x == 'c':
# 		return mock_print_cube(n)


	

  

class ModelTest(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.address_data = Address.objects.create(street='123 abc',
			city='abcity',
			State='abcstate',
			Zip_code = ''
			)
		self.people = People.objects.create(Name='Rahul', 
			age='21', 
			email='rahul@gmail.com', 
			sex='M', 
			height='6', 
			weight='72', 
			relationship='OR', 
			address=self.address_data
			)

	@patch.object(People, 'male',side_effect=mock_male)
	def test_mock_male(self, male):
		url = reverse('male')
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.json()[0]['Name'], 'abc')


class peopleModelTest(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.address_data = Address.objects.create(street='123 abc',
			city='abcity',
			State='abcstate',
			Zip_code = ''
			)
		self.people = People.objects.create(Name='Rahul', 
			age='21', 
			email='rahul@gmail.com', 
			sex='M', 
			height='6', 
			weight='72', 
			relationship='OR', 
			address=self.address_data
			)

	def test_male(self):
		people = People.objects.get(pk=1)
		self.assertEquals(people.male()[0].Name, 'Rahul')




def mock_start():
	print('inside')	
	import IPython; IPython.embed()

	return 'abc'


class MockThread(TestCase):

	@patch.object(threading.Thread, 'start',side_effect=mock_start)
	def test_mock_start(self, start):
		t1 = threading.Thread(target=views.print_square(10), args=(10,))
		t1.start()
		t1.join()
		# self.assertEqual(t1.start(), 'abc')


