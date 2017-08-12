from django.shortcuts import render
import requests
from rest_framework.renderers import TemplateHTMLRenderer
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.http import HttpResponse
import simplejson as json
from django.shortcuts import redirect
from requests.auth import HTTPBasicAuth

from django.contrib.auth.models import User as UserAuth
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from oauth2_provider.models import AccessToken
from TT.settings import OAUTH2_PROVIDER,SERVER_IP
# Create your views here.
def login_page(request):
    return render(request, 'Superadmin/login.html', {})
def dashboardAdmin(request):
	
	
	try:
		tokenSession = AccessToken.objects.get(token=request.session['token'])
		ID = request.session['userid']
		if timezone.now() > tokenSession.expires:
			#print("ERRROR1")
			request.session['token'] = None
			return redirect('/logout_admin')
		else:
			if ID:
				try:
					return render(request, 'Superadmin/helloworld.html', {})
				except:
					return render(request, 'Unauthorized.html', {})
			else:
				return redirect('/logout_admin')
	except:
		print('Token not found')
		return redirect('/logout_admin')
	
@csrf_exempt
def loginAdminSuccess(request):
	username = request.POST.get("user", "")
	password = request.POST.get("password", "")
	print(username,password)
	url = SERVER_IP + "/o/token/"
	payload = "grant_type=password&password="+password+"&username="+username+""
	headers = {
	'content-type': "application/x-www-form-urlencoded",
	'authorization': "Basic bTU4TkRrQUdKWW55SXE1b3ExcHVaTklGbVZ1eTVlbHNkZWhYMDl4bjpIZjI5d1RqUUUxZVVUZzdkS0tnTVRISzhENjlsVEFDR2VSUk93cTFZWE85RnJsZ2xMMWgyT2h3TGdRUDFMWE5IUDVYdDZycXpKUGFzMmlvNW8xRmlWem5mSDlrdnJVUkNxTXRtaXlmekkzTkdhODRqS0puclJFM1U2TGhLbEhuaQ==",
	'cache-control': "no-cache",
	'postman-token': "2aef8a64-1763-d159-6c6d-77b816ffd285"
	}
	response = requests.request("POST", url, data=payload, headers=headers)

	token_json = response.json()
	#print(token_json)
	#print(token_json['access_token'])
	userModel = get_object_or_404(UserAuth, username=username)
	try:
		user = UserAuth.objects.get(id=userModel.id, is_superuser=1)
	except:
		return Response({'detail': "464"}, status=status.HTTP_401_UNAUTHORIZED,
								content_type="applicationjson")
	userAuth = authenticate(username=username,password=password)
	login(request, userAuth)

	request.session['userid'] = userModel.id
	request.session['token'] = token_json['access_token']


	return redirect('/dashboard_admin')
def logout_view(request):
	request.session['token'] = None
	logout(request)
	return render(request, 'Superadmin/login.html', {})
