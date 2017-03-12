from django.shortcuts import get_object_or_404
from gluttonyTw.models import ResProf, Dish, Order, UserOrder
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from djangoApiDec.djangoApiDec import queryString_required, date_proc
from django.http import JsonResponse, Http404
from django.utils import timezone # auto generate create time.
from gluttonyTw.apps import purchaseProc
from gluttonyTw.view.get_user import get_user

# 使用者的訂單資料，可指定當天或特定日期
# @login_required
@date_proc
def user_api(request, date):
	# will return eatuser and user of System.
	EatU, upperuser = get_user(request)

	json = {
		'User': EatU.userName,
		"Date": str(date.date()),
		"FDish": EatU.FDish.DishName if EatU.FDish != None else None,
		"Ftype": EatU.FType.ResType if EatU.FType != None else None,
		'Order': []
	}

	for UOrderObject in EatU.userorder_set.filter(create__date=datetime(date.year, date.month, date.day)):
		tmp = {
			'create': UOrderObject.create,
			'total': int(UOrderObject.total),
			# meal是一個餐點的陣列 裏面的tuple第一位是餐點名稱，第2位是數量
			'meal': [dict(name=SObject.dish.DishName, amount=SObject.amount) for SObject in UOrderObject.smallorder_set.all()]
		}
		json['Order'].append(tmp)
	return JsonResponse(json, safe=False)



# 顯示特定一間餐廳的詳細簡介資料
def join_order(request):
	if request.POST:
		data = request.POST
		data=data.dict()
		if 'res_id' in request.GET and 'order_id' not in request.GET:
			# only supply res_id means you are the one who create a order and that other people to join.	
			res = ResProf.objects.get(id=request.GET['res_id'])
			EatU, upperuser = get_user(request)

			ob = Order.objects.create(restaurant=res, createUser=EatU, create=timezone.localtime(timezone.now()), period=data['period'], total=0, finished=False)
			uorder = UserOrder.objects.create( orderUser=EatU, total=0, order=ob, create=timezone.localtime(timezone.now()) )
			
		elif 'order_id' in request.GET and 'res_id' not in request.GET:
			# only supply order_id means you want to join this order.
			ob = get_object_or_404(Order, id=request.GET['order_id'])
			res = ob.restaurant
		else:
			raise Http404('parameter error')
		
		if ob.isFinished(): raise Http404('api not found')

		# the purchase happens here!
		p = purchaseProc(res, data, request, ob)
		return JsonResponse({"purchase":"success"}, safe=False)

	raise Http404('api should use post')

# 顯示特定一間餐廳的詳細簡介資料
@queryString_required(['res_id'])
def join_order_list(request):
	result = []
	res_id = int(request.GET['res_id'])
	for i in filter(lambda ob:True if not ob.isFinished() and ob.restaurant.id == res_id else False, Order.objects.all()):
		tmp = dict(order_id=i.id, restaurant=i.restaurant.ResName, createUser=i.createUser.userName, period=i.period)
		result.append(tmp)
	return JsonResponse(result, safe=False)