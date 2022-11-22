from django.db import models


class Vacation(models.Model):
    user_name = models.CharField(max_length=100)
    date = models.DateTimeField()
    message = models.TextField(null=True)
    created_at = models.DateTimeField(auto_created=True)
    deleted_at = models.DateTimeField(null=True)

