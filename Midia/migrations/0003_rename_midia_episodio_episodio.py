# Generated by Django 5.1.3 on 2024-11-21 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Midia', '0002_rename_numero_temporada_numero_temporada_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='episodio',
            old_name='midia',
            new_name='episodio',
        ),
    ]