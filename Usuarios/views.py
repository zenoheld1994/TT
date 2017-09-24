#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from .models import Usuarios,Grupos
# Create your views here.
@csrf_exempt
def login_page(request):
	url = "http://"+SERVER_IP+"/v1/everyone/getEscuelas"

	headers = {
		'content-type': "application/json",
		'cache-control': "no-cache",
		'postman-token': "572188b3-a5b1-ba0d-483a-25c212ed488f"
		}

	response = requests.request("GET", url,  headers=headers)
	schools = json.loads(response.text)
	return render(request, 'Superadmin/login.html', {"schools":schools,"SERVER_IP":SERVER_IP})

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
	name2= name.encode('utf8')
	name = name2
	tokenSession = AccessToken.objects.get(token=request.session['token'])
	usuario = request.session['userid']
	if timezone.now() > tokenSession.expires:
		request.session['token'] = None
		return redirect('/logout_admin')
	else:
			url = "http://"+SERVER_IP+"/v1/escuelas"
			payload = "{\n  \"nombre\": \""+name+"\"\n}"
			headers = {
				'authorization': "Bearer " +str(tokenSession),
				'cache-control': "no-cache",
				'content-type': "application/json"
				}
			response = requests.request("POST", url,data=payload, headers=headers)
			status=response.status_code
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

@csrf_exempt
def profesor_create(request):
	name=(request.POST['fullname']).encode('utf8')
	user=(request.POST['name']).encode('utf8')
	school=request.POST['country']
	password=request.POST['password']
	url = "http://"+SERVER_IP+"/v1/everyone/createProfesor"
	payload = "{\n    \"nombre\": \""+name+"\",\n    \"usuario\": \""+user+"\",\n    \"idEscuela\":\""+school+"\",\n    \"contrasena\":\""+password+"\",\n    \"tipoUsuario\":1\n}"
	headers = {
		'cache-control': "no-cache",
		'content-type': "application/json",	
		'postman-token': "a69b6bcd-a95f-7d67-98a3-716d9ffe91c1"
		}
	response = requests.request("POST", url,data=payload, headers=headers)
	status=response.status_code
	print(status)

	url2 = "http://"+SERVER_IP+"/v1/everyone/getEscuelas"

	headers2 = {
		'content-type': "application/json",
		'cache-control': "no-cache",
		'postman-token': "572188b3-a5b1-ba0d-483a-25c212ed488f"
		}

	response2 = requests.request("GET", url2,  headers=headers2)
	schools = json.loads(response2.text)

	try:
		messages.success(request, 'ANY')
		return render(request, 'Superadmin/login.html', {"schools":schools,"SERVER_IP":SERVER_IP})
	except:
		return render(request, 'Superadmin/login.html', {"schools":schools,"SERVER_IP":SERVER_IP})



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
				print(schools)
				return render(request,'Superadmin/school_list.html' , {"SERVER_IP":SERVER_IP,"schools":schools})
			except:
				return render(request, 'Superadmin/Unauthorized.html', {})
	except:
		return redirect('/logout_admin')
	



def user_list(request):
	try:
		tokenSession = AccessToken.objects.get(token=request.session['token'])
		usuario = request.session['userid']
		if timezone.now() > tokenSession.expires:
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
				return render(request,'Superadmin/user_list.html' , {"SERVER_IP":SERVER_IP,"users":users})
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
#Lo de staff
def dashboardStaff(request):
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
					return render(request, 'Superadmin/Welcome_staff.html', {"username":username})
				except:
					return render(request, 'Unauthorized.html', {})
			else:
				return redirect('/logout_admin')
	except:
		print('Token not found')
		return redirect('/logout_admin')

def group_admin(request):
	try:
		tokenSession = AccessToken.objects.get(token=request.session['token'])
		usuario = request.session['userid']
		if timezone.now() > tokenSession.expires:
			request.session['token'] = None
			return redirect('/logout_admin')
		else:
			profesor = Usuarios.objects.get(idUser=usuario)
			if(profesor.idGrupo!=None):
				createoredit=False
				group = Grupos.objects.get(idGrupo=profesor.idGrupo.pk)
				return render(request, 'Superadmin/group_edit.html', {"createoredit":createoredit,
					"group":group,"SERVER_IP":SERVER_IP})
			else:
				createoredit=True
				return render(request, 'Superadmin/group_edit.html', {"createoredit":createoredit})
	except:
		print("valio verga")
		return redirect('/logout_admin')

@csrf_exempt
def group_save(request):
	name=request.POST['group_name']
	tokenSession = AccessToken.objects.get(token=request.session['token'])
	usuario = request.session['userid']
	if timezone.now() > tokenSession.expires:
		request.session['token'] = None
		return redirect('/logout_admin')
	else:
			url = "http://"+SERVER_IP+"/v1/grupos"
			payload = "{\n  \"nombre\": \""+name+"\"\n}"
			headers = {
				'authorization': "Bearer " +str(tokenSession),
				'cache-control': "no-cache",
				'content-type': "application/json",	
				'postman-token': "a69b6bcd-a95f-7d67-98a3-716d9ffe91c1"
				}
			response = requests.request("POST", url,data=payload, headers=headers)
			status=response.status_code
			print(status)
			if(status==200):
				messages.success(request, 'ANY')
				return redirect('/editGroup')
			elif(status==500):
				messages.error(request, 'ANY')
				return redirect('/editGroup')
			return render(request, 'Superadmin/Unauthorized.html', {})
	return redirect('/logout_admin')

#####################################
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
	depends = False
	try:
		user = UserAuth.objects.get(id=userModel.id, is_superuser=1)
		depends = True
	except:
		try:
			user = UserAuth.objects.get(id=userModel.id)
			usuario = Usuarios.objects.get(idUser=userModel.id,tipoUsuario=True)
		except:
			messages.error(request, 'ERROR')
			return redirect('/login_page')
	try:
		userAuth = authenticate(username=username,password=password)
		login(request, userAuth)
	except:
		messages.error(request, 'ERROR')
		return redirect('/login_page')
	try:
	
		request.session['userid'] = userModel.id
		request.session['username'] = username
		request.session['token'] = token_json['access_token']
	except:
		messages.error(request, 'ERROR')
		return redirect('/login_page')

	if(depends):
		return redirect('/dashboard_admin')
	else:
		return redirect('/dashboard_staff')
def logout_view(request):
	request.session['token'] = None
	logout(request)
	return redirect(login_page)
