from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class TE(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.TextField()
    query_date = models.DateTimeField()

    def __str__(self):
        return self.query
