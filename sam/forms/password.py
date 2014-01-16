from django import forms


class PasswordForm(forms.Form):
        password_parts = forms.CharField(max_length=50, label="Password", widget=forms.PasswordInput)
        email_confirmation = forms.CharField(required=False)
