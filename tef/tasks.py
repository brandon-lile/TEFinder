from __future__ import absolute_import
from celery import shared_task
import json
from .models import TE, Solution


@shared_task
def queue_te(te_id):
    te = TE.objects.get(pk=te_id)
    dna_translate = {
        'A': 'T',
        'T': 'A',
        'C': 'G',
        'G': 'C'
    }

    # Get reverse query
    te.reverse_query = ''
    for x in te.query:
        te.reverse_query = dna_translate[x] + te.reverse_query

    str_max = len(te.query) - 1
    cur_pos = str_max
    potentials = {}
    solutions = {}

    # Loop till we hit front of query
    while cur_pos >= 0:
        # Where in the comparison/reverse query we are
        rev_loc = 0

        # Maximum distance in the reverse query we can go
        max_rev = str_max - cur_pos

        # Loop till we hit end of query
        while rev_loc <= max_rev:
            """
            First we need to loop through the query and reverse query and get
            all of the corresponding matches. After that we can look at our
            list of match locations, grab the first index we haven't looked
            at, and go backwards in the list and calculate the following:

            1. Is the distance between the first index and the last above
            our distance minimum
            2. Are the number of indexes between the two divided by the total
            distance greater than our threshold

            If it satisfies the above two conditions, we can create a new solution
            """

            # Where we should be in the original query
            query_loc = cur_pos + rev_loc

            if te.query[query_loc] == te.reverse_query[rev_loc]:
                # We have a base match, check if our cur_pos already has matches
                if cur_pos not in potentials:
                    potentials[cur_pos] = [query_loc]
                else:
                    potentials[cur_pos].append(query_loc)
            rev_loc += 1

        else:
            # See if our potentials for the position meet distance requirements
            if cur_pos in potentials and len(potentials[cur_pos]) > 1:

                # Distance between first and last match
                distance = potentials[cur_pos][-1] - potentials[cur_pos][0]
                if distance >= te.distance:
                    solutions[cur_pos] = potentials[cur_pos]

        cur_pos -= 1

    # Analyze solutions
    analyze_solutions(te, solutions)

    # Update our te
    te.solved = True
    te.save()

    return None


def analyze_solutions(tef, solutions):

    # Loop through each comparison position and analyze the matches
    for pos in solutions:

        # The list of base matches
        matches = solutions[pos]

        tot_matches = len(matches)

        # The base match we're on
        for x in range(0, tot_matches):
            # Base number to start at
            base_num = matches[x]

            # The maximum distance our solution can have
            outer_dist = matches[-1] - base_num
            if outer_dist >= tef.distance:

                # Loop through all inner distances
                for y in range(tot_matches - 1, x - 1 if x != 0 else x, -1):

                    # Check if we are still above distance min
                    inner_dist = matches[y] - base_num
                    if inner_dist >= tef.distance:

                        # Num of matches in distance
                        end_loc = y if y == tot_matches - 1 else y + 1

                        num_matches = len(matches[x:end_loc])

                        # Check if it's above our threshold
                        perc_match = (num_matches / inner_dist) * 100
                        if perc_match >= tef.threshold:

                            # Get solution string
                            soln_str = make_soln_str(tef, matches[x:end_loc])

                            # Create a solution
                            sol = Solution(
                                te=tef,
                                solution=soln_str,
                                percentage=perc_match,
                                distance=inner_dist
                            )
                            sol.save()

                    else:
                        break
            else:
                # List = sorted. Anything past index will be < te.distance
                break


def make_soln_str(tef, bases):
    # Utility vars
    last = bases[-1] if bases[-1] == len(tef.query) - 1 else bases[-1] + 1
    dna_translate = {
        'A': 'T',
        'T': 'A',
        'C': 'G',
        'G': 'C'
    }

    orig_query = tef.query[bases[0]:last]
    soln_str = ''

    # x represents location in orig query
    for x in range(bases[0], bases[-1]):
        if x in bases:
            soln_str += dna_translate[tef.query[x]]
        else:
            soln_str += '-'

    # Combine the two into soln string
    final_str = ''

    if len(soln_str) > 25:
        for i in range(0, len(orig_query), 25):
            # Give the start base
            if i == 0:
                desc_str = "[Base #: " + str(bases[0]) + "]"
                final_str += desc_str \
                         + " ".join(orig_query[i: i + 25]) \
                         + '\r\n' \
                         + "-" * len(desc_str) \
                         + " ".join(soln_str[i: i + 25]) \
                         + '\r\n\r\n'

            final_str += " ".join(orig_query[i: i + 25]) \
                         + '\r\n' \
                         + " ".join(soln_str[i: i + 25]) \
                         + '\r\n\r\n'
    else:
        final_str += " ".join(orig_query) + '\r\n' + " ".join(soln_str)

    return final_str
