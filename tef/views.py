from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
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
    context = {'te': te}

    return render(request, 'tef/review.html', context)
