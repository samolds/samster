from django.shortcuts import render_to_response
from django.template import RequestContext
#from django.contrib.auth.decorators import login_required
#from django.http import HttpResponse
#from django.conf import settings

#@login_required
def contact(request):
    context = RequestContext(request, {})
    return render_to_response('contact.html', {}, context)


#def contact(request):
#    contact_variables = _contact_variables(request, spot_id)
#    if spot_id is None:
#        spot_id = ''
#        displayed_spot_id = 'Unknown'
#    else:
#        displayed_spot_id = spot_id
#
#    back = contact_variables['back']
#    spot_name = contact_variables['spot_name']
#    spot_description = contact_variables['spot_description']
#
#    if request.method == 'POST':
#        form = ContactForm(request.POST)
#        if form.is_valid():
#            name = form.cleaned_data['name']
#            sender = form.cleaned_data['sender']
#            message = form.cleaned_data['message']
#            #feedback_choice = form.cleaned_data['feedback_choice']
#            feedback_choice = 'problem'
#            bot_test = form.cleaned_data['email_confirmation']
#
#            browser = request.META.get('HTTP_USER_AGENT', 'Unknown')
#
#            subject = "SpaceScout %s from %s" % (feedback_choice, name)
#            email_message = "SpaceScout Web - %s \n\n %s \n\n %s %s \n %s - ID = %s \
#                \n Browser Type = %s" % (feedback_choice, message, name, sender, spot_name, displayed_spot_id, browser)
#
#            if bot_test == '':
#                try:
#                    send_mail(subject, email_message, sender, settings.FEEDBACK_EMAIL_RECIPIENT)
#                except:
#                    return HttpResponseRedirect('/sorry/' + spot_id)
#            return HttpResponseRedirect('/thankyou/' + spot_id)
#    else:
#        form = ContactForm()
#
#    return render_to_response('contact-form.html', {
#        'form': form,
#        'back': back,
#        'spot_name': spot_name,
#        'spot_description': spot_description,
#        'spot_id': spot_id,
#    }, context_instance=RequestContext(request))
