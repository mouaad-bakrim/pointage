# Generated by Django 5.1 on 2024-08-15 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personne', '0002_pointeur_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pointeur',
            name='email',
            field=models.EmailField(default='me@gmail.com', max_length=254),
        ),
    ]
