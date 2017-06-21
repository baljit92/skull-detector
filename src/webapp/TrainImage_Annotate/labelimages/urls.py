from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^add/$', views.add, name='addImg'),
	url(r'^view/$', views.viewImg, name='viewImages'),
	url(r'^download/$', views.downloadImg, name='downloadAnnotImages'),
	url(r'^downloadall/$', views.downloadAll, name='downloadAllImages'),
]
