from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
import json
from .forms import SearchForm
from .tasks import queue_te
from .models import TE


# Shows search page
def search(request):

    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            # Create original object
            t = TE(
                query=form.cleaned_data['query'],
                threshold=form.cleaned_data['threshold'],
                start_loc=form.cleaned_data['start_loc'],
                end_loc=form.cleaned_data['end_loc']
            )
            t.save()

            # Throw into celery
            queue_te(t)

            return HttpResponseRedirect(reverse('tef:review', args=(t.id,)))
        else:
            context = {'search_form': form}
            return render(request, 'tef/index.html', context)
    else:
        context = {
            'search_form': SearchForm()
        }
        return render(request, 'tef/index.html', context)


def review(request, te_id):
    te = get_object_or_404(TE, pk=te_id)
    te.solution = json.loads(te.solution)
    dna_translate = {
        'A': 'T',
        'T': 'A',
        'C': 'G',
        'G': 'C'
    }

    # Create generator
    def sol_gen():
        solutions = []
        solns = sorted(te.solution, key=lambda k: len(te.solution[k]), reverse=True)
        for x in solns:
            soln_str = ""
            clean_soln = ""
            for y in range(0, len(te.query)):
                if y in te.solution[x]:
                    clean_soln += dna_translate[te.query[y]]
                    soln_str += dna_translate[te.query[y]]
                else:
                    soln_str += "."
            if soln_str not in solutions:
                solutions.append(soln_str)

                # Ensure we have matching portion too
                soln_str = list(soln_str)
                front_loc = te.query.find(clean_soln[::-1])
                for z in range(front_loc, front_loc + len(clean_soln)):
                    soln_str[z] = dna_translate[te.query[z]]

                # Split string up for readability
                ret_soln = []
                if len(te.query) > 25:
                    for i in range(0, len(te.query), 25):
                        ret_soln.append(
                            (
                                " ".join(te.query[i: i + 25]),
                                " ".join(soln_str[i: i + 25])
                            )
                        )
                else:
                    ret_soln.append((" ".join(te.query), " ".join(soln_str)))

                yield (len(te.solution[x]), ret_soln)

    context = {
        'te': te,
        'solns': sol_gen,
        'orig': " ".join(te.query)
    }

    return render(request, 'tef/review.html', context)
