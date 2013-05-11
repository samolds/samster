from django.shortcuts import render_to_response
from django.template import RequestContext
#from django.contrib.auth.decorators import login_required
#from django.http import HttpResponse
#from django.conf import settings

#@login_required
def home(request):
    context = RequestContext(request, {})
    return render_to_response('home.html', {}, context)
