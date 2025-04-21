from django import forms
from .models import Room, Hashtag,Message

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["hashtag", "name", "information"]
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Enter room name..",
                "class": "form-control",
            }),
            "hashtag": forms.Select(attrs={
                "class": "form-control",
            }),
            "information": forms.Textarea(attrs={
                "placeholder": "Enter room description..",
                "class": "form-control",
                "rows": 4,
            }),
        }
        labels = {
            "hashtag": "HASHTAG",
            "name": "ROOM NAME",
            "information": "ROOM INFORMATION",
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if len(name) < 3:
            raise forms.ValidationError("Room name must be at least 3 characters long.")
        return name

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["chat",]
        widgets = {
            "chat": forms.Textarea(attrs={
                "placeholder":"Enter chat...",
                "class":"form-control",
                "rows":4,
            })
        }
        label = {"chat":"message"}

class HashtagForm(forms.ModelForm):
    class Meta:
        model = Hashtag
        fields = ['name',]
        widgets = {
            "name": forms.TextInput(attrs={
                "class":"form-control",
                "placeholder":"Enter hashtag name..."
            })
        }
        label = {"name":"Hashtag Name"}