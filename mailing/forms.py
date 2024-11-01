from django import forms

from mailing.models import Client, Message, Mailing
from mailing.mixins import StyleFormMixin


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ["full_name", "email", "comment"]


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = ["title", "body"]


class MailingForm(StyleFormMixin, forms.ModelForm):
    send_time = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"},
            format="%Y-%m-%dT%H:%M",
        ),
        input_formats=["%Y-%m-%dT%H:%M"],
        label="Дата и время первой отправки рассылки",
    )

    class Meta:
        model = Mailing
        fields = [
            "send_time",
            "frequency",
            "message",
            "clients",
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        if user.is_superuser:
            self.fields["message"].queryset = Message.objects.all()
            self.fields["clients"].queryset = Client.objects.all()
        else:
            self.fields["message"].queryset = Message.objects.filter(owner=user)
            self.fields["clients"].queryset = Client.objects.filter(owner=user)
        self.apply_widget_classes()
