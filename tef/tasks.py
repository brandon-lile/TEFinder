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

    # Check if we need to change start_loc
    if te.start_loc > 0:
        te.start_loc = min(te.start_loc, len(te.query))

    # Fix query to right size
    working_query = te.query[te.start_loc:te.end_loc + 1]

    te.reverse_query = ''
    for x in te.query:
        te.reverse_query = dna_translate[x] + te.reverse_query

    potential = {}
    str_len = len(working_query) - 1
    cur_pos = str_len
    while cur_pos >= 0:
        rev_loc = 0
        max_rev = str_len - cur_pos
        while rev_loc <= max_rev:
            query_loc = cur_pos + rev_loc
            if working_query[query_loc] == te.reverse_query[rev_loc]:
                if cur_pos not in potential:
                    potential[cur_pos] = [query_loc, str_len - rev_loc]
                else:
                    potential[cur_pos].append(query_loc)
                    potential[cur_pos].append(str_len - rev_loc)
            rev_loc += 1
        else:
            if cur_pos in potential and len(potential[cur_pos]) < te.threshold:
                potential[cur_pos] = []
        cur_pos -= 1

    te.solution = json.dumps(potential)
    te.solved = True
    te.save()
    return None
