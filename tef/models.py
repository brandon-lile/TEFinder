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
    solution = models.TextField(null=True, blank=False)
    start_loc = models.IntegerField(default=0)
    end_loc = models.IntegerField(default=0)

    def __str__(self):
        return self.query
