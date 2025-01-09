from django.urls import path, include
from . import views

app_name = "Midia"

urlpatterns = [
    # we dont have views.login made yet, it's just a pattern to follow
    path("buscar_filme", views.buscar_filme, name="buscar_filme"),
    path("buscar_serie", views.buscar_serie, name="buscar_serie"),
    path("buscar_midia", views.buscar_midia, name="buscar_midia"),
    path("salvar_midia", views.salvar_midia, name="salvar_midia"),
    path("login", views.login, name="login"),
    path("criar_conta", views.criar_conta, name="criar_conta"),

]
