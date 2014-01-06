from django.shortcuts import render_to_response
from django.template import RequestContext


def err_403(request):
    top = "403"
    message = "Forbidden"
    return render_to_response('error.html', {"top": top, "message": message}, context_instance=RequestContext(request))


def err_404(request):
    top = "404"
    message = "Page Not Found"
    return render_to_response('error.html', {"top": top, "message": message}, context_instance=RequestContext(request))


def err_500(request):
    top = "500"
    message = "Server Error"
    return render_to_response('error.html', {"top": top, "message": message}, context_instance=RequestContext(request))
