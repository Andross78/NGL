from django import forms

class AuthorForm(forms.Form):
    author_name = forms.CharField(label='Authors Name', max_length=128, widget=forms.TextInput(attrs={
        "id":"author-name",
        "class":"form-control"
    } ))