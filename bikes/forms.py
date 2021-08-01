from crispy_forms.helper import FormHelper
from django.forms import ModelForm

from .models import Bike


class BikeForm(ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

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
