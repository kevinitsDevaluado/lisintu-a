# Generated by Django 3.0.8 on 2022-08-05 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0004_auto_20220602_2319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='cargo_perfil',
            field=models.CharField(blank=True, max_length=80),
        ),
    ]
