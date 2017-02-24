# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
# Create your models here.
# 要取得會員的model要這樣寫
from userper import Userper
User = Userper('login.stufinite.faith')

class Type(models.Model):
    ResType = models.CharField(max_length=10, null=True)
    def __str__(self):
        return self.ResType

class ResProf(models.Model):
    ResName = models.CharField(max_length=30, null=True) # 餐廳名稱
    address = models.CharField(max_length=30, null=True)
    ResLike = models.PositiveSmallIntegerField(default=50) # always add default value!
    score = models.PositiveSmallIntegerField(default=3)
    last_reserv = models.CharField(max_length=20)
    ResType = models.ManyToManyField(Type) # 餐廳的料理類型
    country = models.CharField(max_length=10) # 哪個國家的餐廳
    avatar = models.ImageField(default='images/time2eat/restaurant.svg') # 大頭貼照片
    environment = models.ImageField(default='images/time2eat/burger.svg') # 店家的環境照片
    envText = models.CharField(max_length=255, default='以新鮮食材佐特製湯頭，搭配風格設計空間，讓聚餐除了享受美食，也能提升時尚品味！')
    feature = models.ImageField(default='images/time2eat/noodles.svg')
    featureText = models.CharField(max_length=255, default='均勻分布的油花與鮮紅肉質，讓口感更加紮實不凡，肉獨有的香氣與油花潤飾，放進精心熬煮清甜的湯汁中輕涮，令人流連忘返的香滑柔嫩口感，讓你感動不已！')
    breakfast = models.CharField(max_length=11, default='6:00-10:00')
    lunch = models.CharField(max_length=11, default='11:00-14:00')
    dinner = models.CharField(max_length=11, default='17:00-21:00')

    def __str__(self):
      return self.ResName

class Menu(models.Model):
    restaurant = models.ForeignKey(ResProf) # 菜單所屬的餐廳
    image = models.ImageField(default='images/time2eat/menu.svg')
    def __str__(self):
        return self.restaurant.__str__()

class Date(models.Model):
    # Date 是用來存星期幾有開店
    DayOfWeek = models.CharField(max_length=1) # 表示星期幾
    Start = models.CharField(max_length=8) # 開始營業時間
    CloseMid = models.CharField(max_length=8, null=True) # 中午結束營業時間（店家中午不一定休息，所以允許空字串）
    StartMid = models.CharField(max_length=8, null=True) # 下午重新開始營業時間（店家中午不一定休息，所以允許空字串）
    Close = models.CharField(max_length=8) # 結束營業時間
    restaurant = models.ForeignKey(ResProf) # 有開店的日子，一對多的關係
    def __str__(self):
        return self.DayOfWeek + self.Start + '~' + self.Close

class Phone(models.Model):
    phoneNum = models.CharField(max_length=15) # 電話號碼
    restaurant = models.ForeignKey(ResProf) # 考慮到一間店可能有多隻聯絡電話
    def __str__(self):
        return self.phoneNum

class Dish(models.Model):
    DishName = models.CharField(max_length=20, null=True) # 菜名
    price = models.PositiveIntegerField(default=0) # 價錢
    isSpicy = models.BooleanField()
    restaurant = models.ForeignKey(ResProf) # 餐點的餐廳
    image = models.ImageField(default='images/time2eat/turkey.svg') # 餐點的照片
    def __str__(self):
        return self.DishName

class EatUser(models.Model):
    # 今天吃什麼的使用者，用來紀錄使用者的飲食習慣
    UpperUser = User
    userName = models.CharField(max_length=30, null=True)
    FDish = models.ForeignKey(Dish, null=True)
    FType = models.ForeignKey(Type, null=True)
    def __str__(self):
        return str(self.UpperUser)

class Comment(models.Model):
    restaurant = models.ForeignKey(ResProf)
    author = models.ForeignKey(EatUser)
    feeling = models.CharField(max_length=200, null=True)
    like = models.PositiveSmallIntegerField(default=1)
    def __str__(self):
        return self.feeling
    def addLike(self):
        self.like += 1

class FavorType(models.Model):
    EatUser = models.ForeignKey(EatUser)
    type = models.ForeignKey(Type, null=True)
    freq = models.PositiveIntegerField() # 紀錄你吃這種類型的餐廳幾次

class FavorDish(models.Model):
    EatUser = models.ForeignKey(EatUser)
    dish = models.ForeignKey(Dish, null=True)
    freq = models.PositiveIntegerField() # 紀錄你常常吃哪一道菜

class ResFavorDish(models.Model):
    # 用來紀錄餐廳的各個餐點受到歡迎的程度
    Res = models.ForeignKey(ResProf)
    dish = models.ForeignKey(Dish, null=True)
    freq = models.PositiveIntegerField(default=0)
    dateOfMon_Year = models.DateTimeField() # 儲存這個月該餐點的銷售量就好


class Order(models.Model):
    # 餐廳的訂單，是一個一對多的關係，因為一間餐廳會有多張訂單
    restaurant = models.ForeignKey(ResProf)
    createUser = models.ForeignKey(EatUser, null=True)
    create = models.DateTimeField() # 訂單的精確時間
    period = models.CharField(max_length=1) # 標示是早中午哪個時段
    total = models.PositiveIntegerField() # 該訂單總額
    finished = models.BooleanField(default=False)
    def __str__(self):
        return str(self.create) + ' ' + str(self.restaurant)
    def isFinished(self):
        if self.finished == True:
            return True
        return False

class UserOrder(models.Model):
    orderUser = models.ForeignKey(EatUser, null=True) # 為了要紀錄使用者有定過哪些菜色（這邊很有問題）
    total = models.PositiveIntegerField() # 該使用者這次定餐的總額
    order = models.ForeignKey(Order) # 隸屬的訂單
    create = models.DateTimeField(null=True) # 訂單的精確時間
    def __str__(self):
        return str(self.orderUser) + str(self.order)

class SmallOrder(models.Model):
    dish = models.ForeignKey(Dish)
    amount = models.PositiveIntegerField()
    UserOrder = models.ForeignKey(UserOrder)
    def __str__(self):
        return str(self.dish) + ' ' + str(self.amount) + '份'
