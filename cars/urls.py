from django.urls import path

from .views import TireInfoView

urlpatterns = [
    path("/tire-info", TireInfoView.as_view()),
]
