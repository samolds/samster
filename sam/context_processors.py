from django.conf import settings


def is_mobile(request):
    """ See if it's mobile mode
    """
    if request.MOBILE == 1:
        return {'is_mobile': True}
    else:
        return {'is_mobile': False}


def is_admin(request):
    """ See if user is logged into the django admin
    """
    if request.user.is_superuser:
        return {'is_admin': True} 
    else:
        return {'is_admin': False}


def github_username(request):
    """ Returns the username set in local_settings.py
    """
    return {'GITHUB_USERNAME': settings.GITHUB['USERNAME']}


def linkedin_username(request):
    """ Returns the username set in local_settings.py
    """
    return {'LINKEDIN_USERNAME': settings.LINKEDIN['USERNAME']}


def sitename(request):
    """ Returns the sitename set in local_settings.py
    """
    return {'SITENAME': settings.SITENAME}


def proper_name(request):
    """ Returns the propername set in local_settings.py
    """
    return {'PROPER_NAME': settings.PROPER_NAME}


def empty_text(request):
    """ Returns the emptytext set in local_settings.py
    """
    return {'EMPTY_TEXT': settings.EMPTY_TEXT}
