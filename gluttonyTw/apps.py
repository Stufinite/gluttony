from django.apps import AppConfig


class GluttonyTwConfig(AppConfig):
    name = 'gluttonyTw'


from django.http import Http404
from django.utils import timezone # auto generate create time.
from gluttonyTw.models import Order, UserOrder, SmallOrder, Dish
from djangoApiDec.djangoApiDec import getJsonFromApi
from gluttonyTw.view.get_user import get_user

class purchaseProc(object):
	"""docstring for purchaseProc"""
	def __init__(self, res, postData, request, ob):
		""" Create a object to handle with the process of placing an order.
		Args:
		    res: restaurant object
		    postDate: the dict data from request.POST
		    request: request object got from django
		    uorder: UserOrder object
		"""
		self.request = request
		self.order = ob
		self.EatU, upperuser = get_user(request)
		self.restaurant = res
		self.cleanPostData = self._verifyPostData(postData)
		self.uorder = UserOrder.objects.create( orderUser=self.EatU, total=0, order=ob, create=timezone.localtime(timezone.now()) )

		self.check()
	
	def _verifyPostData(self, postData):
		""" To verify whether the postData contains some malicious data.
		Returns:
		    A valid dict with only DishName and amounts.
		"""

		def checkValidOrder(dishName):
			if dishName!= 'period' and dishName!= 'csrfmiddlewaretoken' and dishName!='':
				return True
			return False

		jsonText = getJsonFromApi(self.request, 'http', 'gluttonyTw', 'restaurant_menu', (('res_id', self.restaurant.id),))
		menuList = tuple(i['name'] for i in jsonText['dish'])

		cleanPostData = {}
		for i in postData:
			if i not in menuList and checkValidOrder(i):
				raise Http404("api does not exist")
			elif checkValidOrder(i):
				cleanPostData[i] = postData[i]
		return cleanPostData

	def check(self):
		""" Iterate through all item user ordered then calculate the money you need to pay.
		Returns:
		    None.
		"""
		total = 0

		for i in self.cleanPostData.items():
			db = Dish.objects.get(DishName=i[0])
			total+=int(db.price)*int(i[1])
			SmallOrder.objects.create(dish=db, amount=i[1], UserOrder=self.uorder)

		# and then update the real total value into UserOrder
		# UserOrder has the many SmallOrder points to it.
		self.uorder.total = total
		self.uorder.save()

		self.order.total= self.order.total + total
		self.order.save()