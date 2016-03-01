from __future__ import absolute_import
from celery import shared_task


# Solve problem, put in dictionary, json, throw in database
@shared_task
def queue_te(te):
    te.solved = True
    te.save()
    return None
