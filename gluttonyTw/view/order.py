from django.shortcuts import get_object_or_404
from gluttonyTw.models import ResProf, Dish, Order
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from djangoApiDec.djangoApiDec import queryString_required, date_proc
from django.http import JsonResponse, Http404
from gluttonyTw.apps import purchaseProc
from gluttonyTw.view.get_user import get_user

# 使用者的訂單資料，可指定當天或特定日期
# @login_required
@date_proc
def user_api(request, date):
	# will return eatuser and user of System.
	EatU = get_user(request)

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
@queryString_required(['res_id', 'orderId'])
def join_order(request):
	ob = get_object_or_404(Order, id=request.GET['orderId'])
	if ob.isFinished(): raise Http404('api not found')
	res = ResProf.objects.get(id=request.GET['res_id'])

	if request.POST:
		data = request.POST
		data=data.dict()

		p = purchaseProc(res, data, request, ob)

		return JsonResponse({"purchase":"success"}, safe=False)
	raise Http404('you didnt supply post data.')

# 顯示特定一間餐廳的詳細簡介資料
def join_order_list(request):
	result = []
	for i in filter(lambda ob:False if ob.isFinished() else True, Order.objects.all()):
		if i.createUser != None:
			tmp = dict(orderID=i.id, restaurant=i.restaurant.ResName, createUser=i.createUser.userName, period=i.period)
			result.append(tmp)
	return JsonResponse(result, safe=False)