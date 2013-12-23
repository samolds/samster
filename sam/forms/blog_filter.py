from django import forms


class BlogFilterForm(forms.Form):
        tag = forms.CharField(max_length=25, label="Tag", required=False)
        date = forms.CharField(max_length=25, label="Date", required=False)
