from django.conf.urls import include, url
from . import views

urlpatterns = [
	url(r'^login_page$', views.login_page),
	url(r'^dashboard_admin$', views.dashboardAdmin),
	url(r'^admin_successful_login$', views.loginAdminSuccess),
	url(r'^logout_admin$', views.logout_view),
	url(r'^userList$', views.user_list),
]