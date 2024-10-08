# Generated by Django 4.1.1 on 2024-03-30 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('veriproje', '0002_kisi'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dosya',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sinif', models.CharField(max_length=100)),
                ('javaDocSatir', models.DecimalField(decimal_places=2, max_digits=10)),
                ('yorumSatirSayisi', models.DecimalField(decimal_places=2, max_digits=10)),
                ('kodSatir', models.DecimalField(decimal_places=2, max_digits=10)),
                ('loc', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fonksiyonSayisi', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
