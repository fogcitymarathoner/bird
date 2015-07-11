from django import forms

from tpages.models import TokenizedPage
class PageAddForm(forms.Form):
    title = forms.CharField(max_length=100, 
              widget=forms.TextInput(
                 attrs={'size':'100', 'class':'inputText'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'rows':75, 'cols':80}))
    expiration_date = forms.DateField(('%m/%d/%Y',), label='Expiration Date', required=False,  
        widget=forms.DateTimeInput(format='%m/%d/%Y', attrs={
            'class':'input',
            'size':'15'
        })
    )
    
class PageEditForm(forms.ModelForm):
    title = forms.CharField(max_length=100, 
              widget=forms.TextInput(
                 attrs={'size':'100', 'class':'inputText'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'rows':75, 'cols':80}))

    class Meta:
        model = TokenizedPage