from django.urls import path, include
from . import views

app_name = "Midia"

urlpatterns = [
    path("", views.review, name="home"),
    path("profile", views.profile, name="profile"),
    path("buscar_filme", views.buscar_filme, name="buscar_filme"),
    path("buscar_serie", views.buscar_serie, name="buscar_serie"),
    path("buscar_midia", views.buscar_midia, name="buscar_midia"),
    path("salvar_midia", views.salvar_midia, name="salvar_midia"),
    # path("criar_review", views.criar_review, name="criar_review"),
    path("review", views.review, name="review"),
    # path("get_review", views.get_review, name="get_review"),
    path(
        "get_details_review/<int:id_review>/",
        views.get_details_review,
        name="details_review",
    ),
    path("deletar_review/<int:id_review>/", views.deletar_review, name="deletar_review"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("criar_conta", views.criar_conta, name="criar_conta"),
    path("criar_filme", views.criar_filme, name="criar_filme"),
    path(
        "criar_serie_temporada",
        views.criar_serie_temporada,
        name="criar_serie_temporada",
    ),
    path(
        "criar_episodios_temporada",
        views.criar_episodios_temporada,
        name="criar_episodios_temporada",
    ),
    path("seguindo", views.seguindo, name="seguindo"),
    path("buscar_usuarios", views.buscar_usuarios, name="buscar_usuarios"),
]
