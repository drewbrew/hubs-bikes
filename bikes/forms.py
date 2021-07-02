from django.forms import ModelForm

from .models import Bike


class BikeForm(ModelForm):
    class Meta:
        model = Bike
        exclude = [
            "intake_time",
            "marked_as_needing_repair_time",
            "dismantled_time",
            "sold_time",
            "marked_as_ready_for_sale_time",
            "marked_as_ready_for_scrap_time",
        ]
