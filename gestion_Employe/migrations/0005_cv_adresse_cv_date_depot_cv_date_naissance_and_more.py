# Generated by Django 5.1 on 2024-08-28 22:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_Employe', '0004_listestatut_alter_pointage_statut_point_pdf'),
    ]

    operations = [
        migrations.AddField(
            model_name='cv',
            name='adresse',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cv',
            name='date_depot',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='cv',
            name='date_naissance',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cv',
            name='diplomes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cv',
            name='email',
            field=models.EmailField(default='', max_length=255, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cv',
            name='experiences',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cv',
            name='infos_complementaires',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cv',
            name='langages',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cv',
            name='niveau_etude',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cv',
            name='permis_de_conduites',
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='cv',
            name='situation_familiale',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cv',
            name='telephone',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
