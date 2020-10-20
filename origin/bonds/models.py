from django.db import models
from django.conf import settings


class Bond(models.Model):
    isin = models.CharField(max_length=100)
    size = models.IntegerField()
    currency = models.CharField(max_length=5)
    maturity = models.CharField(max_length=10)
    lei = models.CharField(max_length=20)
    legal_name = models.CharField(max_length=200, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True)
