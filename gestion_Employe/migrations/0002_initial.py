# Generated by Django 5.1 on 2024-08-15 00:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gestion_Employe', '0001_initial'),
        ('personne', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pointage',
            name='employe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personne.employe'),
        ),
    ]
