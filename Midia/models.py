from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.forms import ValidationError

# Create your models here.

PERFIS = (
    ("ADMINISTRADOR", "Administrador"),
    ("USUARIO", "Usuário")
)

# POR PADRÃO, O DJANGO JÁ POSSUI UMA CLASSE "USER", que contém campos que todo usuario tem, como username, senha, email
class Usuario(AbstractUser):
    perfil = models.CharField(max_length=40, choices=PERFIS)

    def __str__(self):
        return self.first_name


class Amigo(models.Model):
    usuario1 = models.ForeignKey(
        Usuario, on_delete=models.DO_NOTHING, null=False, related_name="amigo_usuario1"
    )
    usuario2 = models.ForeignKey(
        Usuario, on_delete=models.DO_NOTHING, null=False, related_name="amigo_usuario2"
    )

    def __str__(self):
        return f"{self.usuario1.first_name}-AMIZADE-{self.usuario2.first_name}"


class Midia(models.Model):
    titulo = models.CharField(max_length=255, null=False)
    nota = models.FloatField(null=False)
    data_lancamento = models.DateField(null=False)
    genero = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.titulo


class Review(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, null=False)
    midia = models.ForeignKey(Midia, on_delete=models.DO_NOTHING, null=False)
    comentario = models.CharField(max_length=500, null=False)
    nota = models.FloatField(null=False)

    class Meta:
        unique_together = (("usuario", "midia"),)

    def __str__(self):
        return f"Review-{self.usuario.first_name}-{self.midia.titulo}"


class Filme(models.Model):
    midia = models.OneToOneField(Midia, on_delete=models.DO_NOTHING, null=False)
    duracao = models.IntegerField(null=False)

    def __str__(self):
        return self.midia.titulo


class Temporada(models.Model):
    serie = models.ForeignKey(Midia, on_delete=models.DO_NOTHING, null=False)
    numero_temporada = models.IntegerField(null=False)

    class Meta:
        unique_together = (("serie", "numero_temporada"),)

    def __str__(self):
        return f"{self.serie.titulo}-Temporada-{self.numero_temporada}"


class Episodio(models.Model):
    episodio = models.OneToOneField(Midia, on_delete=models.DO_NOTHING, null=False)
    serie = models.ForeignKey(
        Temporada,
        on_delete=models.DO_NOTHING,
        null=False,
        related_name="episodios_serie",
    )
    numero_temporada = models.ForeignKey(
        Temporada,
        on_delete=models.DO_NOTHING,
        null=False,
        related_name="episodios_temporada",
    )
    numero_episodio = models.IntegerField(null=False)
    duracao = models.IntegerField(null=False)

    class Meta:
        unique_together = (("serie", "numero_temporada", "numero_episodio"),)

    def clean(self):
        # Verifica se a serie possui de fato a temporada
        if not Temporada.objects.filter(
            serie=self.serie.serie,
            numero_temporada=self.numero_temporada.numero_temporada,
        ).exists():
            raise ValidationError(
                f"A temporada {self.numero_temporada.numero} NÃO existe na série {self.serie.serie.titulo}."
            )

    def __str__(self):
        return f"{self.serie.serie.titulo}. Temporada-{self.numero_temporada}. Episodio{self.numero_episodio}"
