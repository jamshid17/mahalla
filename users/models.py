
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.apps import apps


class User(AbstractUser):
    class UserChoice(models.TextChoices):
        NAZORATCHI = 'Nazoratchi', 'Nazoratchi'
        HOKIMIYAT = 'Hokimiyat', 'Hokimiyat'
        KADASTR = 'Kadastr', 'Kadastr'
        QURILISH = "Qurilish", "Qurilish"
        RAIS = 'Rais', 'Rais'
        HOKIM_YORDAMCHISI = 'Hokim yordamchisi', 'Hokim yordamchisi'

    role = models.CharField(
        choices=UserChoice.choices, max_length=200, null=True, blank=True, 
    )
    mahalla = models.ForeignKey(
        to='main.Mahalla', on_delete=models.CASCADE, related_name='user', null=True, blank=True
    )
    tuman = models.ForeignKey(
       to='main.Tuman', on_delete=models.CASCADE, related_name='user', null=True, blank=True
    )

    def __str__(self):
        if self.role == 'Rais' or self.role == 'Hokim yordamchisi':
            return f"MFY: {self.mahalla.name}, {self.mahalla.tuman.name}"
        elif self.role in ['Kadastr', 'Hokimiyat', 'Qurilish', 'Nazoratchi']:
            return f"{self.role}: {self.tuman}"

        else:
            return f"Admin: {self.username}"
