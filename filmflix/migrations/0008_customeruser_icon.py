# Generated by Django 5.0.6 on 2024-09-14 11:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmflix', '0007_alter_icon_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='customeruser',
            name='icon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='filmflix.icon'),
        ),
    ]
