from django.contrib import admin
from .models import Chart, Metric, Lost_site

admin.site.register(Metric)
admin.site.register(Chart)
admin.site.register(Lost_site)
