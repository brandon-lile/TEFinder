from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render
from .tasks import queue_te
from .models import TE


# Shows search page
def index(request):
    all_searches = TE.objects.order_by('query_date')[:5]
    context = {'searches': all_searches}
    return render(request, 'tef/index.html', context)


def search(request):
    # Create original object
    t = TE(
        user=request.user,
        query=request.POST['te_query']
    )
    t.save()

    # Throw into celery
    queue_te(t)

    # Send them to the results page
    return HttpResponse("Search")


def review(request, te_id):
    return HttpResponse()