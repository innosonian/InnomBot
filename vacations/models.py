from django.db import models


class Vacation(models.Model):
    user_name = models.CharField(max_length=100)
    date = models.DateTimeField()


