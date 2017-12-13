from django.conf.urls import url, include
from rest_framework import routers
from quickstart import views
from django.conf.urls import include
from quickstart.views import VisitViewSet, UserViewSet, api_root
from rest_framework import renderers
from rest_framework.schemas import get_schema_view
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

schema_view = get_schema_view(title='Pastebin API')
visit_list =VisitViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
visit_detail = VisitViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve',
	'post': 'create',
	'put': 'update',
	
})

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^$', views.start_page, name ="home"),
	url(r'^schema/$', schema_view),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	#url(r'^', include('quickstart.urls')),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^$', views.api_root),
	url(r'^visits/$', visit_list, name='snippet-list'),
	url(r'^accounts/visits/$', views.visits, name='visits'),
	#url(r'^login/$', views.login_user, name='login'),
    #url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^accounts/profile/$',  views.main, name='main'),
	url(r'^accounts/', include('django.contrib.auth.urls')),
	url(r'^accounts/register/$', views.signup, name='register'),
]