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
