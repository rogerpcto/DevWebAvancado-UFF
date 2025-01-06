from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import PERFIS, Midia
import requests
from django.http import JsonResponse


# Create your views here.
import os
from dotenv import load_dotenv

load_dotenv()
# API_KEY = os.getenv('API_KEY')
URL = "https://tvshow.p.rapidapi.com"
API_HOST = "tvshow.p.rapidapi.com"

HEADERS = {"x-rapidapi-key": os.getenv("API_KEY"), "x-rapidapi-host": API_HOST}


def login(request):

    if request.method == "GET":
        return render(request, "login.html")

    elif request.method == "POST":
        dados = request.POST
        email = dados.get("username")
        senha = dados.get("senha")

        try:
            usuario = User.objects.get(email=email)
        except Exception as erro:
            usuario = None
            messages.add_message(request, constants.ERROR, "Email inválido!")
            return redirect("/")

        usuario_autenticado = auth.authenticate(
            request, username=usuario.username, password=senha
        )
        if usuario_autenticado:
            auth.login(request, usuario_autenticado)
            return redirect("/agenda")
        else:
            messages.add_message(request, constants.ERROR, "Senha inválida!")
            return redirect("/")


def criar_conta(request):
    if request.method == "GET":
        return render(request, "criar_conta.html")

    else:
        dados = request.POST
        nome = dados.get("primeiro-nome").title()
        # last_name = dados.get("ultimo-nome").title()
        email = dados.get("email").strip()
        senha = dados.get("senha")

        if (
            User.objects.filter(email=email).exists()
            or User.objects.filter(username=email).exists()
        ):
            messages.add_message(
                request, constants.WARNING, "Já existe um usuário com esse email"
            )

        else:
            try:
                User.objects.create_user(
                    username=email,
                    first_name=nome,
                    perfil=PERFIS.USUARIO,
                    email=email,
                    password=senha,
                )
                messages.add_message(
                    request, constants.SUCCESS, "Conta criada com sucesso!"
                )

            except Exception as erro:
                print(erro)
                messages.add_message(
                    request, constants.ERROR, "Não foi possível criar conta"
                )
                # return redirect("/")

        return redirect("/")


def buscar_filme(request):

    if request.method == "GET":
        return render(request, "buscar_filme.html")

    if request.method == "POST":
        url = f"{URL}/Movie/Search"
        params_to_search = ["Content"]
        # TO DO: if the media is not in the first page, then we can add a feature to load more medias
        query_string = {"Page": "1", "Language": "pt-BR", "Adult": "true"}
        dados = request.POST
        for param in params_to_search:
            if dados.get(param):
                query_string[param] = dados.get(param)

        response = requests.get(url, headers=HEADERS, params=query_string)
        json_data = response.json()
        medias = []
        properties_to_filter = ["title", "releaseDate", "voteAverage", "genres", "id"]
        for media in json_data:
            if media["originalLanguage"] == "en":
                filtered_media = {
                    key: media[key] for key in properties_to_filter if key in media
                }
                medias.append(filtered_media)
        print(medias)

        return render(request, "buscar_filme.html", {"medias": medias})


def buscar_serie(request):
    if request.method == "GET":
        return render(request, "buscar_filme.html")

    if request.method == "POST":
        dados = request.POST
        url = f"{URL}/Serie/Search"
        params_to_search = ["Content"]
        # TO DO: if the media is not in the first page, then we can add a feature to load more medias
        if dados.get("api_externa"):
            query_string = {"Page": "1", "Language": "pt-BR", "Adult": "true"}
            for param in params_to_search:
                if dados.get(param):
                    query_string[param] = dados.get(param)

            response = requests.get(url, headers=HEADERS, params=query_string)
            json_data = response.json()
            medias = []
            properties_to_filter = [
                "name",
                "releaseDate",
                "voteAverage",
                "genres",
                "id",
            ]
            for media in json_data:
                if media["originalLanguage"] == "en":
                    filtered_media = {
                        key: media[key] for key in properties_to_filter if key in media
                    }
                    medias.append(filtered_media)

        else:
            url = "http://localhost:8000/buscar_midia"  # Ajuste o domínio conforme necessário
            params = {"nome": dados.get("Content")}  # Parâmetro de consulta
            medias = requests.get(url, params=params).json()
        return render(request, "buscar_filme.html", {"medias": medias})


def buscar_midia(request):
    if request.method == "GET":
        nome = request.GET.get("nome", "")
        midias = Midia.objects.filter(titulo=nome)
        if not nome:
            midias = Midia.objects.all()
        midias = list(midias.values())
        if not midias:
            return JsonResponse(
                {"message": "Mídias não encontradas"},
                status=404,  # Código HTTP para "Não Encontrado"
            )
        return JsonResponse(midias, safe=False)
