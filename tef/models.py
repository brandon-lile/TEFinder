from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class TE(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             null=True,
                             blank=False)
    query = models.TextField(blank=False)
    reverse_query = models.TextField(null=True, blank=True)
    threshold = models.IntegerField(default=0)
    query_date = models.DateTimeField(auto_now_add=True)
    solved = models.BooleanField(default=False)
    distance = models.IntegerField(default=0)

    def __str__(self):
        return self.query


class Solution(models.Model):
    search = models.ForeignKey(TE,
                               on_delete=models.CASCADE)
    solution = models.TextField(null=True, blank=False)
    percentage = models.DecimalField(max_digits=3, decimal_places=1)
    distance = models.IntegerField(null=False, blank=False)
