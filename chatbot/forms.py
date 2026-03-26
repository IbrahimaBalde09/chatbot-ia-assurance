from django import forms


class ChatForm(forms.Form):
    question = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Ex : Ma voiture a eu un accident, que dois-je faire ?",
            }
        ),
    )