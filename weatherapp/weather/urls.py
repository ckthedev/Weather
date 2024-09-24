from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # This maps the root URL to the `home` view
]
