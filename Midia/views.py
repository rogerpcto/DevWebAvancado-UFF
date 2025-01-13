from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import (
    PERFIS,
    Midia,
    Review,
    Usuario,
    Amigo,
    Filme,
    Midia,
    Temporada,
    Episodio,
)
import requests
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q

import os
from dotenv import load_dotenv

load_dotenv()
URL = "https://tvshow.p.rapidapi.com"
API_HOST = "tvshow.p.rapidapi.com"

HEADERS = {"x-rapidapi-key": os.getenv("API_KEY"), "x-rapidapi-host": API_HOST}


def login(request):

    if request.method == "GET":
        return render(request, "login.html")

    elif request.method == "POST":
        dados = request.POST
        username = dados.get("username")
        senha = dados.get("senha")

        try:
            usuario = Usuario.objects.get(username=username)
        except Exception as erro:
            print(erro)
            usuario = None
            messages.add_message(request, constants.ERROR, "Email inválido!")
            return redirect("/login")

        usuario_autenticado = auth.authenticate(
            request, username=usuario.username, password=senha
        )
        if usuario_autenticado:
            auth.login(request, usuario_autenticado)
            return redirect("/")
        else:
            messages.add_message(request, constants.ERROR, "Senha inválida!")
            return redirect("/")


def logout(request):
    auth.logout(request)
    return redirect("/login")


def criar_conta(request):
    if request.method == "GET":
        return render(request, "criar_conta.html")

    else:
        dados = request.POST
        nome = dados.get("primeiro-nome").title()
        email = dados.get("email").strip()
        senha = dados.get("senha")

        if (
            Usuario.objects.filter(email=email).exists()
            or Usuario.objects.filter(username=email).exists()
        ):
            messages.add_message(
                request, constants.WARNING, "Já existe um usuário com esse email"
            )

        else:
            try:
                Usuario.objects.create_user(
                    username=email,
                    first_name=nome,
                    perfil="USUARIO",
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

        return redirect("/login")


@login_required(login_url="/login")
def profile(request):
    if request.method == "GET":
        user = Usuario.objects.get(username=request.user.username)
        return render(
            request,
            "profile.html",
            {"user": user, "perfis": ["USUARIO", "ADMINISTRADOR"]},
        )

    elif request.method == "POST":
        dados = request.POST
        nome = dados.get("name")
        email = dados.get("email")
        username = dados.get("username")
        perfil = dados.get("perfil")
        try:
            user = Usuario.objects.filter(username=username).first()
            user.first_name = nome
            user.email = email
            if request.user.perfil == "ADMINISTRADOR":
                user.perfil = perfil
            user.save()
        except Exception as erro:
            print(str(erro))
    return render(
        request, "profile.html", {"user": user, "perfis": ["USUARIO", "ADMINISTRADOR"]}
    )


@login_required(login_url="/login")
def buscar_filme(request):

    if request.method == "GET":
        return render(request, "buscar_filme.html", {"midias": ""})

    if request.method == "POST":
        dados = request.POST

        if dados.get("api_externa").lower() == "true":
            url = f"{URL}/Movie/Search"
            params_to_search = ["content"]
            query_string = {"Page": "1", "Language": "pt-BR", "Adult": "true"}
            for param in params_to_search:
                if dados.get(param):
                    query_string[param] = dados.get(param)

            response = requests.get(url, headers=HEADERS, params=query_string)
            if not response.content:
                return render(
                    request,
                    "buscar_filme.html",
                    {"midia": {}},
                )
            json_data = response.json()
            midias = []
            properties_to_filter = [
                "title",
                "releaseDate",
                "voteAverage",
                "genres",
                "id",
                "image",
            ]
            propriedades = [
                "titulo",
                "data_lancamento",
                "nota",
                "genero",
                "id_midia",
                "imagem",
            ]
            for midia in json_data:
                if midia["originalLanguage"] == "en":
                    filtered_midia = {
                        propriedades[contador]: midia[key]
                        for contador, key in enumerate(properties_to_filter)
                        if key in midia
                    }
                    midias.append(filtered_midia)
        else:
            url = "http://localhost:8000/buscar_midia"
            params = {"nome": dados.get("content")}
            response = requests.get(url, params=params)
            if response.status_code == 404:
                return render(
                    request,
                    "buscar_filme.html",
                    {"midias": {response.json()["message"]}},
                )

            midias = response.json()
        return render(request, "buscar_filme.html", {"midias": midias, "tipo": "filme"})


@login_required(login_url="/login")
def buscar_serie(request):
    if request.method == "GET":
        return render(request, "buscar_filme.html")

    if request.method == "POST":
        dados = request.POST
        url = f"{URL}/Serie/Search"
        params_to_search = ["content"]
        if dados.get("api_externa").lower() == "true":
            query_string = {"Page": "1", "Language": "pt-BR", "Adult": "true"}
            for param in params_to_search:
                if dados.get(param):
                    query_string[param] = dados.get(param)

            response = requests.get(url, headers=HEADERS, params=query_string)
            if not response.content:
                return render(
                    request,
                    "buscar_filme.html",
                    {"midia": {}},
                )
            json_data = response.json()
            midias = []
            properties_to_filter = [
                "name",
                "firstAirDate",
                "voteAverage",
                "genres",
                "id",
                "image",
            ]
            propriedades = [
                "titulo",
                "data_lancamento",
                "nota",
                "genero",
                "id_midia",
                "imagem",
            ]
            for midia in json_data:
                if midia["originalLanguage"] == "en":
                    filtered_midia = {
                        propriedades[contador]: midia[key]
                        for contador, key in enumerate(properties_to_filter)
                        if key in midia
                    }

                    midias.append(filtered_midia)

        else:
            url = "http://localhost:8000/buscar_midia"
            params = {"nome": dados.get("content")}
            response = requests.get(url, params=params)
            if response.status_code == 404:
                return render(
                    request,
                    "buscar_filme.html",
                    {"midias": {response.json()["message"]}},
                )

            midias = response.json()
        return render(request, "buscar_filme.html", {"midias": midias, "tipo": "serie"})


def buscar_midia(request):
    if request.method == "GET":
        nome = request.GET.get("nome", "")
        if not nome:
            midias = Midia.objects.all()
        else:
            midias = Midia.objects.filter(titulo__icontains=nome)
        if not midias:
            return JsonResponse(
                {"message": "Nenhuma Mídia encontrada"},
                status=404,
            )
        midias = list(midias.values())
        return JsonResponse(midias, safe=False)

@csrf_exempt
def salvar_midia(request):
    if request.method == "POST":
        try:
            midia_data = json.loads(request.body).get("midia")
            titulo = midia_data.get("titulo")
            data_lancamento = midia_data.get("data_lancamento")
            nota = midia_data.get("nota")
            genero = midia_data.get("genero")
            id = midia_data.get("id")
            poster = midia_data.get("poster")
            midia = Midia.objects.create(
                titulo=titulo,
                data_lancamento=data_lancamento,
                nota=nota,
                genero=genero,
                id_midia=id,
                poster=poster,
            )

            if json.loads(request.body).get("tipo_midia") == "filme":
                url = "http://localhost:8000/criar_filme"
                params = {"id_midia": midia.id_midia}
                response = requests.post(url, params=params)

            elif json.loads(request.body).get("tipo_midia") == "serie":
                url = "http://localhost:8000/criar_serie_temporada"
                params = {"id_midia": midia.id_midia}
                response = requests.post(url, params=params)
                if response.status_code == 200:
                    url = "http://localhost:8000/criar_episodios_temporada"
                    params = {"id_midia": midia.id_midia}
                    response = requests.post(url, params=params)

        except Exception as erro:
            if "UNIQUE" in str(erro):
                return JsonResponse({"error": "Mídia já cadastrada"}, status=403)
            return JsonResponse({"error": str(erro)}, status=400)

    return JsonResponse(
        {"message": "Data received", "data": midia.id_midia}, status=200
    )


@csrf_exempt
def criar_serie_temporada(request):
    if request.method == "POST":
        midia_id = request.GET.get("id_midia", "")
        try:
            midia = Midia.objects.filter(id_midia=int(midia_id)).first()
            if midia:
                url = f"{URL}/Serie/Detail"
                query_string = {"Items": midia.id_midia, "Language": "pt-BR"}
                response = requests.get(url, headers=HEADERS, params=query_string)
                numero_de_temporadas = int(response.json()[0]["numberOfSeasons"])
                for temporada in range(1, (numero_de_temporadas + 1)):
                    Temporada.objects.create(serie=midia, numero_temporada=temporada)
                return JsonResponse(
                    {"message": "As temporadas da série foram criadas com sucesso!"},
                    status=200,
                )
        except Exception as erro:
            return JsonResponse({"status": "error", "message": str(erro)}, status=400)


@csrf_exempt
def criar_episodios_temporada(request):
    if request.method == "POST":
        midia_id = request.GET.get("id_midia", "")
        midia = Midia.objects.filter(id_midia=int(midia_id)).first()
        if midia:
            serie_temporadas = Temporada.objects.filter(serie=midia).order_by(
                "numero_temporada"
            )
            quantidade_temporadas = serie_temporadas.count()
            if quantidade_temporadas == 0:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": f"A midia com o id {midia_id} não corresponde a uma série. Ou as temporadas dessa mídia ainda não foram criadas.",
                    },
                    status=400,
                )
            url = f"{URL}/Serie/Episodes"
            for temporada in serie_temporadas:
                query_string = {
                    "ItemId": temporada.serie.id_midia,
                    "Language": "pt-BR",
                    "SeasonNumber": temporada.numero_temporada,
                }
                response = requests.get(url, headers=HEADERS, params=query_string)
                json_data = response.json()
                properties_to_filter = [
                    "name",
                    "airDate",
                    "voteAverage",
                    "id",
                    "episodeNumber",
                    "runtime",
                    "image",
                ]
                propriedades = [
                    "titulo",
                    "data_lancamento",
                    "nota",
                    "id_midia",
                    "numero_episodio",
                    "duracao",
                    "imagem",
                ]
                for episode in json_data:
                    filtered_midia = {
                        propriedades[contador]: episode[key]
                        for contador, key in enumerate(properties_to_filter)
                        if key in episode
                    }
                    if all(value is None for value in filtered_midia.values()):
                        continue
                    try:
                        episodio = Midia.objects.create(
                            id_midia=filtered_midia["id_midia"],
                            titulo=filtered_midia["titulo"],
                            data_lancamento=filtered_midia["data_lancamento"],
                            nota=filtered_midia["nota"],
                            poster=filtered_midia["imagem"],
                        )

                        Episodio.objects.create(
                            episodio=episodio,
                            serie_temporada=temporada,
                            numero_episodio=filtered_midia["numero_episodio"],
                            duracao=filtered_midia["duracao"],
                        )
                    except Exception as erro:
                        return JsonResponse(
                            {"status": "error", "message": str(erro)}, status=400
                        )
        return JsonResponse(
            {"message": "Todos os Episódios da série foram adicionados com sucesso!"},
            status=200,
        )

def listar_reviews(request):
    if request.method == "GET":
        user_reviews = Review.objects.filter(usuario=request.user).order_by(
            "midia__titulo"
        )
        if not user_reviews:
            return JsonResponse(
                {"message": "O Usuário ainda não possui Reviews de uma mídia"},
                status=404,
            )
        user_reviews = list(user_reviews.values())
        return JsonResponse(user_reviews, safe=False)


@csrf_exempt
def criar_filme(request):
    if request.method == "POST":
        midia_id = request.GET.get("id_midia", "")
        # midia_id = json.loads(request.body).get("id_midia")
        try:
            midia = Midia.objects.filter(id_midia=int(midia_id)).first()
            if midia:
                url = f"{URL}/Movie/Detail"
                query_string = {"Items": midia.id_midia, "Language": "pt-BR"}
                response = requests.get(url, headers=HEADERS, params=query_string)
                json_data = response.json()
                duracao = json_data[0]["runtime"]
                if duracao:
                    Filme.objects.create(midia=midia, duracao=int(duracao))
                    return JsonResponse(
                        {"message": "Filme criado com sucesso!"}, status=200
                    )
                else:
                    return
            else:
                return JsonResponse(
                    {"status": "error", "message": "Mídia não encontrada!"}, status=400
                )

        except Exception as erro:
            return JsonResponse({"status": "error", "message": str(erro)}, status=400)

@csrf_exempt
def buscar_usuarios(request):
    if request.method == "GET":
        nome_usuario = request.GET.get("nome", "")
        if not nome_usuario:
            usuarios = Usuario.objects.all()
        else:
            usuarios = Usuario.objects.filter(first_name__icontains=nome_usuario)
        usuarios = usuarios.values("id", "first_name")
        return JsonResponse(list(usuarios), safe=False)


def fazer_amizade(request):
        dados = request.POST
        id_amigo = dados.get("id_amigo")
        if id_amigo:
            amigo = Usuario.objects.get(id=id_amigo)
        if amigo:
            try:
                Amigo.objects.create(usuario1=request.user, usuario2=amigo)
                amigos = Amigo.objects.filter(usuario1=request.user)
                return render(request, "seguindo.html", {"usuario": request.user, "amigos": amigos})
            except Exception:
                print(Exception)


def desfazer_amizade(request):
        dados = request.POST
        id_amigo = dados.get("id_amigo")
        usuario = Usuario.objects.get(username=request.user.username)
        amigo = Usuario.objects.get(id=id_amigo)
        try:
            amizade1 = Amigo.objects.get(usuario1=usuario, usuario2=amigo)
        except Exception as erro:
            print(erro)
            return JsonResponse(
                {"message": "Não foi encontrada amizade entre os usuários"},
                status=401,
            )
        amizade1.delete()
        amigos = Amigo.objects.filter(usuario1=usuario)
        return render(request,"seguindo.html", {"usuario": usuario,"amigos": amigos}) 


def buscar_amigos(request):
    if request.method == "GET":
        query = Amigo.objects.filter(usuario1=request.user)
        amigos = list(query.values)
        if not amigos:
            return JsonResponse(
                {"message": "O usuário não possui amigos"},
                status=401,
            )
        return JsonResponse(amigos, safe=False)

@csrf_exempt
def listar_amigos(request):
    if request.method == "GET":
        amigos = list(Amigo.objects.all().values("usuario1__first_name", "usuario2__first_name"))
        if not amigos:
            return JsonResponse({"message": "Nenhum amigo encontrado."}, status=404)
        return JsonResponse({"amigos": amigos}, safe=False, status=200)

@csrf_exempt    
def criar_amizade(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            usuario1_id = data["usuario1"]
            usuario2_id = data["usuario2"]

            if Amigo.objects.filter(
                (Q(usuario1_id=usuario1_id) & Q(usuario2_id=usuario2_id)) |
                (Q(usuario1_id=usuario2_id) & Q(usuario2_id=usuario1_id))
            ).exists():
                return JsonResponse({"message": "Eles já são amigos."}, status=400)

            amigo = Amigo.objects.create(usuario1_id=usuario1_id, usuario2_id=usuario2_id)

            return JsonResponse({"message": "Amizade criada", "id": amigo.id}, status=201)
        
        except KeyError:
            return JsonResponse({"error": "Campos 'usuario1' e 'usuario2' são obrigatórios."}, status=400)
        except Exception as erro:
            return JsonResponse({"error": str(erro)}, status=500)

@login_required(login_url="/login")
def review(request):

    if request.method == "GET":
        # se usuario ja tiver feito review daquela midia iria dar problema.
        midia_id = request.GET.get("id_midia")
        if midia_id:
            midia = Midia.objects.filter(id_midia=midia_id).first()
            review = Review.objects.filter(midia=midia, usuario=request.user).first()
            if review:
                review.nota = int(review.nota)
                return render(request, "editar_review.html", {"review": review})
            else:
                return render(
                    request,
                    "criar_review.html",
                    {"midia": midia},
                )
        else:
            reviews = Review.objects.filter(usuario=request.user)
            return render(request, "home.html", {"reviews": reviews})

    if request.method == "POST":
        dados = request.POST
        midia_id = dados.get("id_midia")
        id_review = dados.get("id_review")
        nota = dados.get("nota")
        comentario = dados.get("comentario")
        if midia_id:
            try:
                midia = Midia.objects.get(id_midia=midia_id)
                Review.objects.create(
                    usuario=request.user,
                    midia=midia,
                    nota=nota,
                    comentario=comentario,
                )
                messages.add_message(
                    request, constants.SUCCESS, "Review adicionada com sucesso!"
                )
            except Exception as erro:
                print(erro)
                messages.add_message(
                    request, constants.ERROR, "Não foi possível adicionar a review"
                )
            return redirect("/")

        elif id_review:
            if id_review:
                review = Review.objects.filter(id=id_review).first()
                if review:
                    if (
                        request.user.perfil == "ADMINISTRADOR"
                        or review.usuario.username == request.user.username
                    ):
                        review.comentario = comentario
                        review.nota = nota
                        review.save()
                        return redirect("/")


def amigos(request):
    if request.method == 'GET':
        nome_usuario = request.GET.get("nome", "")
        usuarios = None
        if nome_usuario:
            url = "http://localhost:8000/buscar_usuarios"
            params = {"nome": nome_usuario}
            response = requests.get(url, params=params)
            if response.status_code == 200:
                usuarios = response.json()
                # usuarios = Usuario.objects.filter(first_name=nome_usuario.title())
        amigos = Amigo.objects.filter(usuario1=request.user)        
        return render(request, "seguindo.html", {"amigos": amigos, "usuarios": usuarios} )
        


def deletar_review(request, id_review):
    if request.method == "POST":
        review = Review.objects.filter(id=id_review).first()
        if review:
            if (
                request.user.perfil == "ADMINISTRADOR"
                or review.usuario.username == request.user.username
            ):
                review.delete()
                return redirect("/")


def seguindo(request):
    if request.method == "GET":
        nome_usuario = request.GET.get("nome", "")
        usuarios = []
        if nome_usuario:
            url = "http://localhost:8000/buscar_usuarios"
            params = {"nome": nome_usuario}
            response = requests.get(url, params=params)
            if response.status_code == 200:
                usuarios = response.json()
        amigos = Amigo.objects.filter(usuario1=request.user)        
        for amigo in amigos:
            print(amigo.usuario2.email) 
    return render(request, "seguindo.html", {"amigos": amigos, "usuarios":usuarios})
    
def review_seguindo(request):
    if request.method == "GET":
        amigo  = Usuario.objects.get(id=request.GET.get("id_amigo"))
        reviews = Review.objects.filter(usuario=amigo)
        return render(request, "review_seguindo.html", {"amigo": amigo,"reviews": reviews})

def get_details_review(request, id_review):
    if request.method == "GET":
        if id_review:
            review = Review.objects.filter(id=id_review).first()
            review.nota = int(review.nota)
            return render(request, "editar_review.html", {"review": review})

@csrf_exempt
def reviews(request):
    if request.method == "GET":
        midia_id = request.GET.get("midia_id")
        
        if midia_id:
            reviews = Review.objects.filter(midia_id=midia_id).select_related("midia", "usuario")
        else:
            reviews = Review.objects.all().select_related("midia", "usuario")

        formatted_reviews = []
        for review in reviews:
            formatted_reviews.append({
                "usuario": {
                    "first_name": review.usuario.first_name,
                },
                "comentario": review.comentario,
                "nota": review.nota,
                "midia": {
                    "id": review.midia.id_midia,
                    "titulo": review.midia.titulo,
                    "data_lancamento": review.midia.data_lancamento,
                    "nota": review.midia.nota,
                    "genero": review.midia.genero,
                    "poster": review.midia.poster,
                }
            })

        return JsonResponse(formatted_reviews, safe=False)
    elif request.method == "POST":
        data = json.loads(request.body)
        review = Review.objects.create(**data)
        return JsonResponse({"message": "Review criada", "id": review.id}, status=201)