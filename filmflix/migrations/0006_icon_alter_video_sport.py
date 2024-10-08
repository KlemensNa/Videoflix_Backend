# Generated by Django 5.0.6 on 2024-09-14 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmflix', '0005_alter_video_category_alter_video_sport'),
    ]

    operations = [
        migrations.CreateModel(
            name='Icon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='icons/')),
            ],
        ),
        migrations.AlterField(
            model_name='video',
            name='sport',
            field=models.CharField(choices=[('golf', 'Golf'), ('football', 'Fußball'), ('handball', 'Handball'), ('basketball', 'Basketball'), ('boxing', 'Boxen'), ('skate', 'Skateboard'), ('baseball', 'Baseball'), ('amFootball', 'American Football')], default='', max_length=20),
        ),
    ]
