from django.shortcuts import render_to_response
from django.template import RequestContext


def around_the_web(request):
    return render_to_response('around_the_web.html', {}, context_instance=RequestContext(request))
