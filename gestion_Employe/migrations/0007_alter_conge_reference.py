# Generated by Django 5.1 on 2024-08-29 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_Employe', '0006_remove_conge_document_conge_date_demande_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conge',
            name='reference',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
