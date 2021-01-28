from django.contrib import admin

from .models import Bike, Make, Repair

class BikeAdmin(admin.ModelAdmin):
    list_select_related = ['make']
    list_display = ['id', 'make', 'model', 'serial_number', 'status']


class RepairAdmin(admin.ModelAdmin):
    list_select_related = ['user', 'bike__make']
    list_display = ['id', 'bike', 'user', 'time_finished']


admin.site.register(Make)
admin.site.register(Bike, BikeAdmin)
admin.site.register(Repair, RepairAdmin)
