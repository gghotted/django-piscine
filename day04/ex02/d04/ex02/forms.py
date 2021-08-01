from django import forms


class IndexForm(forms.Form):
    msg = forms.CharField()
