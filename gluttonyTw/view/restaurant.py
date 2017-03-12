from django.shortcuts import get_object_or_404
from django.views import View
from gluttonyTw.models import ResProf, Dish, Type
from datetime import datetime, date
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from djangoApiDec.djangoApiDec import queryString_required, date_proc, queryString_required_ClassVersion

# 顯示餐廳當天或特定日期的訂單資料
# @login_required
@date_proc
@queryString_required(['res_id'])
def rest_api(request, date):
    Res = get_object_or_404(ResProf, id=request.GET['res_id'])  # 回傳餐廳物件
    Res = ResProf.objects.get(id=request.GET['res_id'])  # 回傳餐廳物件

    result = {
        "ResName": Res.ResName,
        "ResAddress": Res.address,
        "Score": int(Res.score),
        "Type": list(map(lambda t:str(t), Res.ResType.all())),
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
@queryString_required(['start'])
def restaurant_list(request):
    start = int(request.GET['start']) - 1 # 因為index是從0開始算，可是人類習慣講從第一筆到第十五筆，所以在這邊幫人類-1
    gap = int(request.GET['gap']) if 'gap' in request.GET else 15
    resObject = ResProf.objects.all()[start::gap]
    json = list(map(lambda i:dict(res_id=i.id, ResName=i.ResName, ResLike = int(i.ResLike), score = int(i.score),  avatar = 'http://' + request.get_host() + i.avatar.url), resObject))
    return JsonResponse(json, safe=False)


# 顯示特定一間餐廳的菜單
@queryString_required(['res_id'])
def restaurant_menu(request):
    resObject = get_object_or_404(ResProf, id=request.GET['res_id'])
    json = {
        "menu" : list(map(lambda x: 'http://' + request.get_host() + x.image.url, resObject.menu_set.all())), 
        "dish" : list(map( lambda i:
            {
                "name" : i.DishName,
                "price" : int(i.price),
                "isSpicy" : i.isSpicy,
                "image" :'http://' + request.get_host() + i.image.url
            }, resObject.dish_set.all() ))
    }

    return JsonResponse(json, safe=False)


# 顯示特定一間餐廳的詳細簡介資料
@queryString_required(['res_id'])
def restaurant_prof(request):
    resObject = get_object_or_404(ResProf, id=request.GET['res_id'])
    json = {
        "ResName" : resObject.ResName,
        "address" : resObject.address,
        "ResLike" : int(resObject.ResLike),
        "score" :   int(resObject.score),
        "last_reserv" : resObject.last_reserv,
        "country" : resObject.country,
        "avatar" : 'http://' + request.get_host() + resObject.avatar.url,
        "environment" : 'http://' + request.get_host() + resObject.environment.url,
        "envText" : resObject.envText,
        "feature" : 'http://' + request.get_host() + resObject.feature.url,
        "featureText" : resObject.featureText
    }
    json['phone'] = list(map(lambda i: str(i), resObject.phone_set.all()))
    json['ResFavorDish'] = list(map(lambda i: (i.dish.DishName.__str__(), int(i.freq)), resObject.resfavordish_set.all() ))
    json['date'] = list(map(lambda i:i.DayOfWeek, resObject.date_set.all()))

    return JsonResponse(json, safe=False)

class ResComment(View):    
    # 顯示特定一間餐廳的評論留言
    @queryString_required_ClassVersion(['res_id'])
    def get(self, request, *args, **kwargs):
        import json
        from django.core import serializers
        from gluttonyTw.view.get_user import get_user
        Res = get_object_or_404(ResProf, id=request.GET['res_id'])  # 回傳餐廳物件
        EatU, upperuser = get_user(request)

        start = int(request.GET['start']) - 1
        comment_list = Res.comment_set.order_by('-like')[start:start+15]
        return JsonResponse(json.loads(serializers.serialize('json', list(comment_list), fields=('author', 'feeling', 'like'))), safe=False)

    def post(self, request, *args, **kwargs):
        from django.core import serializers
        from gluttonyTw.view.get_user import get_user
        Res = get_object_or_404(ResProf, id=request.GET['res_id'])  # 回傳餐廳物件
        EatU, upperuser = get_user(request)

        data = request.POST
        data = data.dict()
        Comment.objects.create(restaurant=Res, author=EatU, feeling=data['feeling'], like=0)
        return JsonResponse({'reply':'success'})