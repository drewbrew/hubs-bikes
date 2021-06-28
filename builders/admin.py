from django.contrib import admin

from . import models


class KidAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]
    list_select_related = ["user"]


admin.site.register(models.Kid, KidAdmin)
admin.site.register(models.Guardian)
