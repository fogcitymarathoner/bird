from django import forms

from tpages.models import TokenizedPage

class PageForm(forms.ModelForm):
    expiration = forms.DateField()

    class Meta:
        model = TokenizedPage
        fields = ['title', 'body']