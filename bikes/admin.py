from django.contrib import admin

from .models import Bike, Donor, Make, Repair


class BikeAdmin(admin.ModelAdmin):
    list_select_related = ["make"]
    list_display = ["id", "make", "model", "serial_number", "status"]
    date_hierarchy = "intake_time"
    fieldsets = [
        (
            "Basic information",
            {
                "fields": (
                    "make",
                    "model",
                    "serial_number",
                    "picture",
                    "status",
                    "donated_by",
                )
            },
        ),
        (
            "More details",
            {
                "fields": (
                    "condition",
                    "frame_size",
                    "wheel_size",
                    "tube_fitting",
                    "brake_type",
                )
            },
        ),
        ("Repair info", {"fields": ("refurb_parts_used", "notes")}),
        (
            "Timestamps",
            {
                "fields": (
                    "intake_time",
                    "marked_as_needing_repair_time",
                    "marked_as_ready_for_sale_time",
                    "sold_time",
                    "dismantled_time",
                )
            },
        ),
    ]


class RepairAdmin(admin.ModelAdmin):
    list_select_related = ["user", "bike__make"]
    list_display = ["id", "bike", "user", "time_finished"]


admin.site.register(Donor)
admin.site.register(Make)
admin.site.register(Bike, BikeAdmin)
admin.site.register(Repair, RepairAdmin)
