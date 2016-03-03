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
        total = 0
        in_sol = False
        for x in range(cur_pos, str_len):
            # Compare base by base
            if working_query[x] == te.reverse_query[x - cur_pos]:
                total += 1
                if total >= te.threshold and in_sol is False:
                    in_sol = True
                    potential[cur_pos] = [x for x in range(x - te.threshold + 1, x)]
                    potential[cur_pos].append(x)
                elif total >= te.threshold and in_sol is not False:
                    potential[cur_pos].append(x)
            else:
                in_sol = False
                total = 0

        cur_pos -= 1

    te.solution = json.dumps(potential)
    te.solved = True
    te.save()
    return None
