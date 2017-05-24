from django.contrib import admin
from .models import User, Site, Chart, Metric, Lost_site

admin.site.register(User)
admin.site.register(Site)
admin.site.register(Metric)
admin.site.register(Chart)
admin.site.register(Lost_site)
