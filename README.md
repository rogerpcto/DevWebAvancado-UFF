# DevWebAvancado-UFF
Trabalho da matéria de Desenvolvimento Web Avançado durante o curso de bacharelado de Sistemas de Informação. Consiste de um projeto de um sistema para avaliação e gerenciamento de Filmes e Séries assistidos pelos usuários.

# Documentação
A pasta documentação contém o relatório sobre as especificações do sistema, assim como anotações de reuniões do grupo, diagramas e projetos de Banco de Dados. Nessa pasta também se encontra a documentação da API em OpenAPI.

# Configurando o Projeto

## 1- Crie o ambiente virtual na raiz do Projeto
- python -m venv venv

<br>

## 2- Ative o ambiente virtual
- venv\Scripts\activate

<br>

## 3- Instale as dependências necessárias
- pip install -r requirements.txt

<br>

## 4- Aplique as alterações do banco de dados (se existir)
- python manage.py makemigrations
- python manage.py migrate

<br>

# Rodando o Projeto
- python manage.py runserver
