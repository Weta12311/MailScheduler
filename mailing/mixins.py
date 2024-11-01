from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, render


class StyleFormMixin:
    default_classes = {
        forms.TextInput: "validate",
        forms.EmailInput: "validate",
        forms.PasswordInput: "validate",
        forms.DateTimeInput: "validate",
        forms.Textarea: "materialize-textarea",
        forms.Select: "input-field",
        forms.SelectMultiple: "input-field",
    }

    def apply_widget_classes(self):
        for field_name, field in self.fields.items():
            widget = field.widget
            widget_class = self.default_classes.get(type(widget))
            if widget_class:
                widget.attrs.setdefault("class", widget_class)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_widget_classes()


class AuthenticationLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy("users:login")

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                "Только авторизованные пользователи могут просматривать данную информацию",
            )
            return redirect(self.login_url)
        return super().handle_no_permission()


class PermissionResponseMixin(PermissionRequiredMixin):
    permission_denied_message = "У вас нет разрешения на доступ к этой странице"

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, self.permission_denied_message)
            return redirect(self.login_url)
        return super().handle_no_permission()
