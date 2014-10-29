from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.cache import cache
from sam.models import Quote


def quote(request):
  quotes = cache.get("quotes")
  if not quotes:
      quotes = list(Quote.objects.filter(private=False))
      cache.set("quotes", quotes)
  return render_to_response('quotes.html', {"quotes": quotes}, context_instance=RequestContext(request))
