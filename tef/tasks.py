from __future__ import absolute_import
from celery import shared_task
import json


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
    #if te.end_loc > 0 and te.end_loc > te.start_loc:
    #    te.end_loc = min(te.end_loc, len(te.query))
    #elif 0 < te.end_loc < te.start_loc:
    #    te.end_loc = te.start_loc
    #elif te.end_loc == 0:
    #    te.end_loc = len(te.query)

    #original_query = te.query
    # May have to change this - indexes could be made wonky above
    #te.query = te.query[te.start_loc:te.end_loc]

    te.reverse_query = ''
    for x in te.query:
        te.reverse_query = dna_translate[x] + te.reverse_query

    potential = {}
    str_len = len(te.query) - 1
    cur_pos = str_len
    while cur_pos >= 0:
        total = 0
        in_sol = False
        for x in range(cur_pos, str_len):
            # Compare base by base
            if te.query[x] == te.reverse_query[x - cur_pos]:
                total += 1
                if total >= te.threshold and in_sol is False:
                    in_sol = True
                    potential[cur_pos] = [x for x in range(x - te.threshold, x)]
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
