from django.shortcuts import render_to_response
from django.template import RequestContext


def sha1(request):
    return render_to_response('sha1.html', {
    }, context_instance=RequestContext(request))
