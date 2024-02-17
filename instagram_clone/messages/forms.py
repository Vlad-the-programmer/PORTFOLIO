from django import forms
from .models import Message


class MessageCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('message', 'image')