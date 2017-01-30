from django.shortcuts import get_object_or_404
from userper import Userper
from gluttony_tw.models import EatUser

# 透過川哲寫的userper套件，利用同一個session抓到系統的會員資料
def get_user(request):
	# use session to determine your user id
	# so use it to find user's EatUser object instance.
	session = request.session.session_key
	upperuser = Userper('login.stufinite.faith')
	upperuser.get_test(session)
	EatU = get_object_or_404(EatUser, userName=upperuser.name)
	return EatU, upperuser