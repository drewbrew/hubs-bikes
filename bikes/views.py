from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render

from .forms import BikeForm
from .models import Bike


def home(request: HttpRequest) -> HttpResponse:
    queryset = Bike.objects.select_related("make")
    return render(request, "bikes/bike-list.html", context={"bikes": queryset.all()})


class BikeCreateView(CreateView):
    model = Bike
    form_class = BikeForm
    template_name = "bikes/bike-detail.html"


class BikeUpdateView(UpdateView):
    model = Bike
    queryset = Bike.objects.select_related("make")
    form_class = BikeForm
    template_name = "bikes/bike-detail.html"
