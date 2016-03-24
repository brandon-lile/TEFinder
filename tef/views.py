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
                threshold=form.cleaned_data['threshold']
            )
            t.save()

            # Throw into celery
            queue_te(t.id)

            return HttpResponseRedirect(reverse('tef:review', args=(t.id,)))
        else:
            context = {'search_form': form}
            return render(request, 'tef/index.html', context)
    else:
        context = {
            'search_form': SearchForm(),
            'title': 'Search'
        }
        return render(request, 'tef/index.html', context)


def review(request, te_id):
    te = get_object_or_404(TE, pk=te_id)

    if te.solved is True and te.solution != "{}":
        te.solution = json.loads(te.solution)
    dna_translate = {
        'A': 'T',
        'T': 'A',
        'C': 'G',
        'G': 'C'
    }

    # Create generator
    all_soln = []
    solns = sorted(te.solution.values(), key=len, reverse=True)
    for x in solns:
        matches = 0
        if x is not None:
            soln_str = ""
            for y in range(0, len(te.query)):
                if y in x:
                    soln_str += dna_translate[te.query[y]]
                    matches += 1
                else:
                    soln_str += "."

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

            all_soln.append((matches, ret_soln))

    context = {
        'te': te,
        'solns': all_soln,
        'title': 'Review'
    }

    return render(request, 'tef/review.html', context)
