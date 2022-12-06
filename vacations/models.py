from django.db import models


class User(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class VacationType(models.Model):
    name = models.CharField(max_length=256)
    weight = models.DecimalField(max_digits=3, decimal_places=1)

    def __str__(self):
        return self.name


class Vacation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    message = models.TextField(null=True)
    vacation_type = models.ForeignKey(VacationType, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_created=True, blank=True, auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
