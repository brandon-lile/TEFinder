from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
import json
from .forms import SearchForm
from .tasks import queue_te
from .models import TE, Solution


# Shows search page
def search(request):

    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            # Create original object
            t = TE(
                query=form.cleaned_data['query'],
                threshold=form.cleaned_data['threshold'],
                distance=form.cleaned_data['distance']
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

    if te.solved:
        solved = True

    soln = Solution.objects.filter(te=te_id).order_by('-percentage')

    context = {
        'te': te,
        'solved': solved,
        'soln': soln,
        'soln_count': soln.count(),
        'title': 'Review'
    }

    return render(request, 'tef/review.html', context)
