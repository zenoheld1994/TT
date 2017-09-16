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
from TT.settings import OAUTH2_PROVIDER,SERVER_IP,BASIC_TOKEN
from django.contrib import messages
# Create your views here.
def login_page(request):
    return render(request, 'Superadmin/login.html', {})

def school_create(request):
	try:
		tokenSession = AccessToken.objects.get(token=request.session['token'])
		usuario = request.session['userid']
		if timezone.now() > tokenSession.expires:
			#print("ERRROR1")
			request.session['token'] = None
			return redirect('/logout_admin')
		else:
			try:
				return render(request, 'Superadmin/school_create.html', {})
			except:
				return render(request, 'Superadmin/Unauthorized.html', {},status=403)
	except:
		return redirect('/logout_admin')
@csrf_exempt
def school_save(request):
	name=request.POST['school_name']
	tokenSession = AccessToken.objects.get(token=request.session['token'])
	usuario = request.session['userid']
	if timezone.now() > tokenSession.expires:
		#print("ERRROR1")
		request.session['token'] = None
		return redirect('/logout_admin')
	else:
			url = "http://"+SERVER_IP+"/v1/escuelas"
			payload = "{\n  \"nombre\": \""+name+"\"\n}"
			headers = {
			    'authorization': "Bearer " +str(tokenSession),
			    'cache-control': "no-cache",
			    'content-type': "application/json",	
			    'postman-token': "a69b6bcd-a95f-7d67-98a3-716d9ffe91c1"
			    }
			response = requests.request("POST", url,data=payload, headers=headers)
			status=response.status_code
			print(status,"aqui we")
			print(response.text)
			print(name)
			try:
				if(status==201):
					messages.success(request, 'ANY')
					return redirect('/schoolCreate')
				elif(status==500):
					messages.error(request, 'ANY')
					return redirect('/schoolCreate')
			except:
				return render(request, 'Superadmin/Unauthorized.html', {})
	return redirect('/logout_admin')

def school_list(request):
	try:
		tokenSession = AccessToken.objects.get(token=request.session['token'])
		usuario = request.session['userid']
		if timezone.now() > tokenSession.expires:
			#print("ERRROR1")
			request.session['token'] = None
			return redirect('/logout_admin')
		else:
			try:
				url = "http://"+SERVER_IP+"/v1/escuelas/"
				headers = {
				    'authorization': "Bearer " +str(tokenSession),
				    'cache-control': "no-cache",
				    'postman-token': "a69b6bcd-a95f-7d67-98a3-716d9ffe91c1"
				    }
				response = requests.request("GET", url, headers=headers)
				schools = json.loads(response.text)
				return render(request,'Superadmin/school_list.html' , {"SERVER_IP":SERVER_IP,"schools":schools["results"]})
			except:
				return render(request, 'Superadmin/Unauthorized.html', {})
	except:
		return redirect('/logout_admin')
	



def user_list(request):
	try:
		tokenSession = AccessToken.objects.get(token=request.session['token'])
		usuario = request.session['userid']
		if timezone.now() > tokenSession.expires:
			#print("ERRROR1")
			request.session['token'] = None
			return redirect('/logout_admin')
		else:
			try:
				url = "http://"+SERVER_IP+"/v1/usuarios/"
				headers = {
				    'authorization': "Bearer " +str(tokenSession),
				    'cache-control': "no-cache",
				    'postman-token': "a69b6bcd-a95f-7d67-98a3-716d9ffe91c1"
				    }
				response = requests.request("GET", url, headers=headers)
				users = json.loads(response.text)
				return render(request,'Superadmin/user_list.html' , {"SERVER_IP":SERVER_IP,"users":users["results"]})
			except:
				return render(request, 'Superadmin/Unauthorized.html', {})
	except:
		return redirect('/logout_admin')
	

def dashboardAdmin(request):
	
	
	try:
		tokenSession = AccessToken.objects.get(token=request.session['token'])
		ID = request.session['userid']
		if timezone.now() > tokenSession.expires:
			request.session['token'] = None
			return redirect('/logout_admin')
		else:
			if ID:
				try:
					request.session['userid']
					username = request.session['username']
					return render(request, 'Superadmin/Welcome.html', {"username":username})
				except:
					return render(request, 'Unauthorized.html', {})
			else:
				return redirect('/logout_admin')
	except:
		print('Token not found')
		return redirect('/logout_admin')
	
@csrf_exempt
def loginAdminSuccess(request):
	username = request.POST.get("username", "")
	password = request.POST.get("password", "")
	url = "http://"+SERVER_IP + "/o/token/"
	payload = "grant_type=password&password="+password+"&username="+username
	headers = {
	'content-type': "application/x-www-form-urlencoded",
	'authorization': "Basic "+BASIC_TOKEN,
	'cache-control': "no-cache",
	'postman-token': "cba85345-7c4f-f0fc-c3f3-f2e86bfca26c"
	}
	try:
		response = requests.request("POST", url, data=payload, headers=headers)
	except:
		return render({'detail': "464"}, status=status.HTTP_401_UNAUTHORIZED,
								content_type="applicationjson")

	token_json = response.json()

	userModel = get_object_or_404(UserAuth, username=username)
	try:
		user = UserAuth.objects.get(id=userModel.id, is_superuser=1)
	except:
		return Response({'detail': "464"}, status=status.HTTP_401_UNAUTHORIZED,
								content_type="applicationjson")
	userAuth = authenticate(username=username,password=password)
	login(request, userAuth)

	request.session['userid'] = userModel.id
	request.session['username'] = username
	request.session['token'] = token_json['access_token']


	return redirect('/dashboard_admin')
def logout_view(request):
	request.session['token'] = None
	logout(request)
	return redirect(login_page)
