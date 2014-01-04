from django.shortcuts import render_to_response
from django.template import RequestContext
from sam.models import Quote


def quote(request):
  quotes = list(Quote.objects.filter(private=False))
  return render_to_response('quotes.html', {"quotes": quotes}, context_instance=RequestContext(request))
