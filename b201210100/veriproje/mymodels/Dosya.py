from django.db import models

class Dosya2(models.Model):
    sinif = models.CharField(max_length=255)
    javadoc_sayisi = models.IntegerField()
    yorum_sayisi = models.IntegerField()
    kod_sayisi = models.IntegerField()
    loc_sayisi = models.IntegerField()
    fonksiyon_sayisi = models.IntegerField()
    yorum_sapma_yuzdesi = models.FloatField()