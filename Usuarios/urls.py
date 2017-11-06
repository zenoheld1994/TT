#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from . import views

urlpatterns = [
	url(r'^login_page$', views.login_page),
	url(r'^dashboard_admin$', views.dashboardAdmin),
	url(r'^admin_successful_login$', views.loginAdminSuccess),
	url(r'^logout_admin$', views.logout_view),
	url(r'^userList$', views.user_list),
	url(r'^schoolCreate$', views.school_create),
	url(r'^saveSchool$', views.school_save),
	url(r'^schoolList$', views.school_list),
	url(r'^login_page_create$', views.profesor_create),
	url(r'^login_page_create_alumno$', views.alumno_create),
	url(r'^dashboard_staff$', views.dashboardStaff),
	#url(r'^scoreList$', views.score_list),puntuaciones_list
	url(r'^puntuacionesList$', views.puntuaciones_list),
	url(r'^leccionList$', views.leccion_list),
	url(r'^dashboard_student$', views.dashboardStudent),
	url(r'^editGroup$', views.group_admin),
	url(r'^saveGroup$', views.group_save),
	url(r'^studentList$', views.alumno_list),
	
]