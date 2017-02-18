from django.contrib import admin
from gluttonyTw.models import Type, ResProf, Date, Phone, Dish, Order, SmallOrder, EatUser, FavorType, FavorDish, ResFavorDish, UserOrder, Menu, Comment
# Register your models here.
admin.site.register(Type)
admin.site.register(ResProf)
admin.site.register(Date)
admin.site.register(Phone)
admin.site.register(Dish)
admin.site.register(Order)
admin.site.register(SmallOrder)
admin.site.register(EatUser)
admin.site.register(FavorType)
admin.site.register(FavorDish)
admin.site.register(ResFavorDish)
admin.site.register(UserOrder)
admin.site.register(Menu)
admin.site.register(Comment)
class ResProf(admin.ModelAdmin):
    list_display = ('ResName', 'ResType', 'score')
    search_fields = ('ResName',)
