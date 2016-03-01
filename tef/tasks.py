from __future__ import absolute_import
from celery import shared_task


# Solve problem, put in dictionary, json, throw in database
@shared_task
def queue_te(te):
    dna_translate = {
        'A': 'T',
        'T': 'A',
        'C': 'G',
        'G': 'C'
    }

    te.reverse_query = ''
    for x in te.query:
        te.reverse_query = dna_translate[x] + te.reverse_query

    te.save()
    return None
