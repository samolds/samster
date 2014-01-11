from django.shortcuts import render_to_response
from django.template import RequestContext
from sam.models import WebSite


def around_the_web(request):
    sites = WebSite.objects.filter(private=False)
    personals = []
    maintains = []
    develops = []
    for site in sites:
        if site.kind == "prsl":
            personals.append(site)
        elif site.kind == "mntn":
            maintains.append(site)
        elif site.kind == "dvlp":
            develops.append(site)

    return render_to_response('around_the_web.html', {
        "personals": personals,
        "maintains": maintains,
        "develops": develops,
    }, context_instance=RequestContext(request))
