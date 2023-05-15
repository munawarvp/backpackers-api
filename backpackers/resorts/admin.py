from django.contrib import admin
from .models import Location, Resorts, Adventures, Destinations

# Register your models here.

admin.site.register(Location)
admin.site.register(Resorts)
admin.site.register(Adventures)
admin.site.register(Destinations)
