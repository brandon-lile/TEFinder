from __future__ import absolute_import
from celery import shared_task
import json
from .models import TE


@shared_task
def queue_te(te_id):
    te = TE.objects.get(pk=te_id)
    dna_translate = {
        'A': 'T',
        'T': 'A',
        'C': 'G',
        'G': 'C'
    }

    
    return None
