from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import PERFIS, Midia, Review, Usuario, Amigo
import requests
from django.http import JsonResponse
from django.db.models import Q


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
        dados = request.POST

        if dados.get("api_externa").lower() == "true":
            url = f"{URL}/Movie/Search"
            params_to_search = ["Content"]
            # TO DO: if the media is not in the first page, then we can add a feature to load more medias
            query_string = {"Page": "1", "Language": "en-US", "Adult": "true"}
            for param in params_to_search:
                if dados.get(param):
                    query_string[param] = dados.get(param)

            response = requests.get(url, headers=HEADERS, params=query_string)
            json_data = response.json()
            medias = []
            properties_to_filter = [
                "title",
                "releaseDate",
                "voteAverage",
                "genres",
                "id",
            ]
            propriedades = ["Titulo", "Data_Lançamento", "Nota", "Genero", "id"]
            for media in json_data:
                if media["originalLanguage"] == "en":
                    filtered_media = {
                        propriedades[contador]: media[key]
                        for contador, key in enumerate(properties_to_filter)
                        if key in media
                    }
                    medias.append(filtered_media)
        else:
            url = "http://localhost:8000/buscar_midia"  # Ajuste o domínio conforme necessário
            params = {"nome": dados.get("Content")}  # Parâmetro de consulta
            response = requests.get(url, params=params)
            if response.status_code == 404:
                return render(
                    request,
                    "buscar_filme.html",
                    {"medias": {response.json()["message"]}},
                )

            medias = response.json()
        return render(request, "buscar_filme.html", {"medias": medias})


def buscar_serie(request):
    if request.method == "GET":
        return render(request, "buscar_filme.html")

    if request.method == "POST":
        dados = request.POST
        url = f"{URL}/Serie/Search"
        params_to_search = ["Content"]
        # TO DO: if the media is not in the first page, then we can add a feature to load more medias
        if dados.get("api_externa").lower() == "true":
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
            propriedades = ["Titulo", "Data_Lançamento", "Nota", "Genero", "id"]
            for media in json_data:
                if media["originalLanguage"] == "en":
                    filtered_media = {
                        propriedades[contador]: media[key]
                        for contador, key in enumerate(properties_to_filter)
                        if key in media
                    }

                    medias.append(filtered_media)

        else:
            url = "http://localhost:8000/buscar_midia"  # Ajuste o domínio conforme necessário
            params = {"nome": dados.get("Content")}  # Parâmetro de consulta
            response = requests.get(url, params=params)
            if response.status_code == 404:
                return render(
                    request,
                    "buscar_filme.html",
                    {"medias": {response.json()["message"]}},
                )

            medias = response.json()
        return render(request, "buscar_filme.html", {"medias": medias})


def buscar_midia(request):
    if request.method == "GET":
        nome = request.GET.get("nome", "")
        if not nome:
            midias = Midia.objects.all()
        else:
            midias = Midia.objects.filter(titulo=nome)
        if not midias:
            return JsonResponse(
                {"message": "Mídias não encontradas"},
                status=404,  # Código HTTP para "Não Encontrado"
            )
        midias = list(midias.values())
        return JsonResponse(midias, safe=False)


def listar_reviews(request):
    if request.method == "GET":
        user_reviews = Review.objects.filter(usuario=request.user).order_by(
            "midia__titulo"
        )
        if not user_reviews:
            return JsonResponse(
                {"message": "O Usuário ainda não possui Reviews de uma mídia"},
                status=404,  # Código HTTP para "Não Encontrado"
            )
        user_reviews = list(user_reviews.values())
        return JsonResponse(user_reviews, safe=False)


def buscar_usuarios(request):
    if request.method == "GET":
        nome_usuario = request.GET.get("nome", "")
        if not nome_usuario:
            usuarios = Usuario.objects.all()
        else:
            usuarios = Usuario.objects.filter(first_name=nome_usuario)
        usuarios = list(usuarios.values)
        return JsonResponse(usuarios, safe=False)


def fazer_amizade(request):
    if request.method == "GET":
        dados = request.POST
        id_amigo = dados.get("id_amigo")
        if id_amigo:
            amigo = Usuario.objects.get(id=id_amigo)
        if amigo:
            try:
                Amigo.objects.create(usuario1=request.user, usuario2=amigo)
                Amigo.objects.create(usuario1=amigo.user, usuario2=request.user)
            except Exception:
                print(Exception)


def desfazer_amizade(request):
    if request.method == "DELETE":
        dados = request.POST
        id_amigo = dados.get("id_amigo")
        amigo = Usuario.objects.get(id=id_amigo)
        try:
            amizade1 = Amigo.get(usuario1=request.user, usuario2=amigo)
            amizade2 = Amigo.get(usuario1=amigo, usuario2=request.user)
        except Exception:
            return JsonResponse(
                {"message": "Não foi encontrada amizade entre os usuários"},
                status=401,  # Código HTTP para "Não Encontrado"
            )
        amizade1.delete()
        amizade2.delete()
        return JsonResponse({"message": "Amizade desfeita com sucesso!"}, status=200)


def buscar_amigos(request):
    if request.method == "GET":
        query = Amigo.objects.filter(usuario1=request.user)
        amigos = list(query.values)
        if not amigos:
            return JsonResponse(
                {"message": "O usuário não possui amigos"},
                status=401,  # Código HTTP para "Não Encontrado"
            )
        return JsonResponse(amigos, safe=False)
