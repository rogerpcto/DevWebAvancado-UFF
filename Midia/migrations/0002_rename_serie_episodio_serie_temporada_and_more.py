# Generated by Django 5.1.3 on 2025-01-09 20:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Midia', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='episodio',
            old_name='serie',
            new_name='serie_temporada',
        ),
        migrations.AlterUniqueTogether(
            name='episodio',
            unique_together={('serie_temporada', 'numero_episodio')},
        ),
        migrations.RemoveField(
            model_name='episodio',
            name='numero_temporada',
        ),
    ]
