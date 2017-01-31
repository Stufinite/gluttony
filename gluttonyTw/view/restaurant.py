from django.shortcuts import get_object_or_404
from gluttonyTw.models import ResProf, Dish, Type
from datetime import datetime, date
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from djangoApiDec.djangoApiDec import queryString_required, date_proc

# 顯示餐廳當天或特定日期的訂單資料
# @login_required
@date_proc
@queryString_required(['res_id'])
def rest_api(request, date):
	Res = get_object_or_404(ResProf, id=request.GET['res_id'])  # 回傳餐廳物件

	result = {
		"ResName": Res.ResName,
		"ResAddress": Res.address,
		"Score": int(Res.score),
		"Type": [str(t) for t in Res.ResType.all()],
		"OrderList": [],
		"Date": str(date.date())
	}
	# 篩選出特定日期的訂單物件, 而且一定要是finished=True代表已經截止揪團
	for OrderObject in Res.order_set.filter(create__date=datetime(date.year, date.month, date.day), finished=False):

		json = {
			'total': int(OrderObject.total),
			'ResOrder': {},
			"Create": OrderObject.create,
			"OrderId" : OrderObject.id
		}

		# 迭代訂單所有的使用者
		for uOrder in OrderObject.userorder_set.all():
			# 迭代一個使用者所訂的所有餐點
			for sOrder in uOrder.smallorder_set.all():
				json['ResOrder'][sOrder.dish.DishName] = json['ResOrder'].setdefault(sOrder.dish.DishName, 0)+int(sOrder.amount)
		result['OrderList'].append(json)

	return JsonResponse(result, safe=False)



# 顯示所有餐廳的簡略資料
def restaurant_list(request):
	json = []
	resObject = ResProf.objects.all()
	for i in resObject:
		tempT = dict(ResName=i.ResName, ResLike = int(i.ResLike), score = int(i.score),  avatar = i.avatar.url)
		json.append(tempT)
	return JsonResponse(json, safe=False)


# 顯示特定一間餐廳的菜單
@queryString_required(['res_id'])
def restaurant_menu(request):
	resObject = get_object_or_404(ResProf, id=request.GET['res_id'])
	json = dict(menu = [i.image.url for i in resObject.menu_set.all()], dish = [ dict(name = i.DishName, price = int(i.price), isSpicy = i.isSpicy, image= i.image.url) for i in resObject.dish_set.all() ] )

	return JsonResponse(json, safe=False)


# 顯示特定一間餐廳的詳細簡介資料
@queryString_required(['res_id'])
def restaurant_prof(request):
	resObject = get_object_or_404(ResProf, id=request.GET['res_id'])
	json = dict(ResName = resObject.ResName, address = resObject.address, ResLike = int(resObject.ResLike), score = int(resObject.score), last_reserv = resObject.last_reserv, country = resObject.country, avatar = resObject.avatar.url, environment = resObject.environment.url, envText = resObject.envText, feature = resObject.feature.url, featureText = resObject.featureText)
	json['phone'] = [str(i) for i in resObject.phone_set.all() ]
	json['ResFavorDish'] = [ (i.dish.DishName.__str__(), int(i.freq)) for i in resObject.resfavordish_set.all() ]
	json['date'] = [ i.DayOfWeek for i in resObject.date_set.all() ]

	return JsonResponse(json, safe=False)
