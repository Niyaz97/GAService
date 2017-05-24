from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.front, name='front'),
    url(r'^sign/in/$', views.sign_in, name='sign_in'),
    url(r'^sign/up/$', views.sign_up, name='sign_up'),
    url(r'^sign/out/$', views.sign_out, name='sign_out'),
    url(r'^analytic$', views.analitic, name='analytic'),
    url(r'^ajax.json$', views.ajax_json, name='ajax_json'),
    url(r'^google/reg$', views.google_reg, name='google_reg'),
]