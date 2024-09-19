# Generated by Django 5.0.6 on 2024-09-14 11:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmflix', '0009_alter_customeruser_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customeruser',
            name='icon',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='filmflix.icon'),
        ),
    ]