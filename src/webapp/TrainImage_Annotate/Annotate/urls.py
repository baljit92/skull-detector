from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^add/$', views.add, name='addImg'),
	url(r'^view/$', views.viewAnnotImgs, name='viewImages'),
	url(r'^viewNMS/$', views.viewAnnotImgsNMS, name='viewNMSImages'),
	url(r'^download/$', views.downloadImgs, name='downloadAnnotImages'),
	url(r'^downloadNMS/$', views.downloadImgsNMS, name='downloadAnnotImages'),
	url(r'^downloadall/$', views.downloadAll, name='downloadAllImages'),
]
