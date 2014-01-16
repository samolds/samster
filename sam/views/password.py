from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from sam.forms.password import PasswordForm
from django.conf import settings
from hashlib import sha1


def password(request):
    password = None
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            raw_password = form.cleaned_data['password_parts']
            bot_test = form.cleaned_data['email_confirmation']

            if bot_test == '':
                salt = sha1(settings.PASSWORD_SALT).hexdigest()
                password = sha1(salt + raw_password).hexdigest()
    else:
        form = PasswordForm()

    return render_to_response('password.html', {
        'form': form,
        'password': password,
    }, context_instance=RequestContext(request))
