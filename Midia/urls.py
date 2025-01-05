from django.urls import path, include
from . import views

app_name = "Midia"

urlpatterns = [
    # we dont have views.login made yet, it's just a pattern to follow
    path('buscar_filme', views.buscar_filme, name='buscar_filme'),
]
