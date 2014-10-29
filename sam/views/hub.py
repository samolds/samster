from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.cache import cache
from django.conf import settings
from sam.models import Website


def hub(request):
    hub = cache.get("hub")
    if not hub:
        sites = Website.objects.filter(private=False)
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

        cache_obj = {
            "personals": personals,
            "maintains": maintains,
            "develops": develops,
        }
        cache.set("hub", cache_obj, settings.CACHE_LENGTH)
    else:
        personals = hub['personals']
        maintains = hub['maintains']
        develops = hub['develops']

    return render_to_response('hub.html', {
        "personals": personals,
        "maintains": maintains,
        "develops": develops,
    }, context_instance=RequestContext(request))
