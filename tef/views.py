from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
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
                user=request.user,
                query=request.POST['te_query']
            )
            t.save()

            # Throw into celery
            queue_te(t)

            return HttpResponseRedirect('tef:review', args=(t.id,))
        else:
            context = {'search_form': form}
            return render(request, 'tef/index.html', context)
    else:
        context = {
            'search_form': SearchForm()
        }
        return render(request, 'tef/index.html', context)


def review(request, te_id):
    return HttpResponse()
