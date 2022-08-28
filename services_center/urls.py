from django.urls import path
from . import views

urlpatterns = [
    path('service-register', views.ServiceRegister.as_view())
]
