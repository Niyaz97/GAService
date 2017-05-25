from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.front, name='front'),
    url(r'^out/$', views.sign_out, name='out'),
    url(r'^analitic$', views.analitic, name='analitic'),
    url(r'^ajax.json$', views.ajax_json, name='ajax_json'),
    url(r'^reg$', views.reg, name='reg'),
    url(r'^chart$', views.chart, name='chart'),
]