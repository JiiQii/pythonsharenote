from django import forms

class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea,required=False)
