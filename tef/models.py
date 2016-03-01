from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


# Create your models here.
class TE(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             null=True,
                             blank=False)
    query = models.TextField(blank=False)
    query_date = models.DateTimeField(auto_now_add=True)
    solved = models.BooleanField(default=False)

    def __str__(self):
        return self.query
