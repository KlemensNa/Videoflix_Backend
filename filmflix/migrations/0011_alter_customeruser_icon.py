# Generated by Django 5.0.6 on 2024-09-15 10:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmflix', '0010_alter_customeruser_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customeruser',
            name='icon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='filmflix.icon'),
        ),
    ]
