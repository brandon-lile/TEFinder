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

    # Check if we need to change start_loc
    if te.start_loc > 0:
        te.start_loc = min(te.start_loc, len(te.query))

    # Check if we need to change end_loc
    if te.end_loc > 0 and te.end_loc > te.start_loc:
        te.end_loc = min(te.end_loc, len(te.query))
    elif te.end_loc > 0 and te.end_loc < te.start_loc:
        te.end_loc = te.start_loc
    elif te.end_loc == 0:
        te.end_loc = len(te.query)

    original_query = te.query
    te.query = te.query[start_loc:end_loc] # May have to change this - indexes could be made wonky above

    te.reverse_query = ''
    for x in te.query:
        te.reverse_query = dna_translate[x] + te.reverse_query

    te.save()
    return None
