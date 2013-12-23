from django import forms


class ContactForm(forms.Form):
        private = forms.BooleanField(required=False)
        name = forms.CharField(max_length=25, label="Your Name")
        email = forms.EmailField(max_length=50, label="Your Email (Optional)", required=False)
        subject = forms.CharField(max_length=50, label="The Subject of Your Message")
        message = forms.CharField(widget=forms.Textarea(), label="Your Message")
        email_confirmation = forms.CharField(required=False)
