# Generated by Django 5.0.6 on 2024-06-11 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmflix', '0002_video_category_video_sport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='category',
            field=models.CharField(choices=[('', ''), ('US-Sport', 'US-Sport'), ('Ballsport', 'Ballsport')], default='', max_length=20),
        ),
    ]
