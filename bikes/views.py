from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render

from .models import Bike


def home(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        queryset = Bike.objects.select_related("make")
    return render(request, "bikes/bike-list.html", context={"bikes": queryset.all()})
