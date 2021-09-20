from django.db import models
from django.contrib.auth.models import User


class CustomUser(User):
    money = models.IntegerField()
    bet = models.IntegerField()
