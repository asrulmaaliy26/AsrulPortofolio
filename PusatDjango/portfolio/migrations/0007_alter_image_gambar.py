# Generated by Django 3.2.12 on 2024-10-19 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0006_auto_20241019_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='gambar',
            field=models.ImageField(blank=True, default='profil.png', null=True, upload_to='profiles/', verbose_name='Image'),
        ),
    ]
