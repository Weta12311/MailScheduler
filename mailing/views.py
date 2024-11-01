import json

from django.contrib import messages
from django.core.cache import cache
from django.db.models import ProtectedError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    TemplateView,
    View,
)

from blog.models import Article
from mailing.forms import ClientForm, MessageForm, MailingForm
from mailing.models import Client, Message, Mailing, MailingAttempt
from mailing.mixins import (
    AuthenticationLoginRequiredMixin as AuthLogin,
    PermissionResponseMixin,
)


class HomePageView(TemplateView):
    template_name = "mailing/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Планировщик Рассылок"

        total_mailings = cache.get("total_mailings")
        if total_mailings is None:
            total_mailings = Mailing.objects.count()
            cache.set("total_mailings", total_mailings, 60 * 5)
        context["total_mailings"] = total_mailings

        active_mailings = cache.get("active_mailings")
        if active_mailings is None:
            active_mailings = Mailing.objects.filter(is_active=True).count()
            cache.set("active_mailings", active_mailings, 60 * 5)
        context["active_mailings"] = active_mailings

        unique_clients = cache.get("unique_clients")
        if unique_clients is None:
            unique_clients = Client.objects.distinct().count()
            cache.set("unique_clients", unique_clients, 60 * 5)
        context["unique_clients"] = unique_clients

        context["random_articles"] = Article.objects.order_by("?")[:3]
        return context


class ClientListView(AuthLogin, PermissionResponseMixin, ListView):
    model = Client
    paginate_by = 6
    ordering = ("-id",)
    permission_required = "mailing.view_client"

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Client.objects.all()
        return Client.objects.filter(owner=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Клиенты рассылки"
        return context


class ClientDetailView(AuthLogin, PermissionResponseMixin, DetailView):
    model = Client
    permission_required = "mailing.view_client"


class ClientCreateView(AuthLogin, PermissionResponseMixin, CreateView):
    model = Client
    form_class = ClientForm
    permission_required = "mailing.add_client"
    success_url = reverse_lazy("mailing:client_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавить нового клиента"
        context["button_text"] = "Добавить"
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)




class ClientUpdateView(AuthLogin, PermissionResponseMixin, UpdateView):
    model = Client
    form_class = ClientForm
    permission_required = "mailing.change_client"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование клиента"
        context["button_text"] = "Сохранить изменения"
        return context

    def get_success_url(self):
        return reverse_lazy("mailing:client_detail", kwargs={"pk": self.object.pk})


class ClientDeleteView(AuthLogin, PermissionResponseMixin, DeleteView):
    model = Client
    success_url = reverse_lazy("mailing:client_list")
    permission_required = "mailing.delete_client"


class MessageListView(AuthLogin, PermissionResponseMixin, ListView):
    model = Message
    paginate_by = 6
    permission_required = "mailing.view_message"

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Message.objects.all()
        return Message.objects.filter(owner=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Сообщения рассылки"
        return context


class MessageDetailView(AuthLogin, PermissionResponseMixin, DetailView):
    model = Message
    permission_required = "mailing.view_message"


class MessageCreateView(AuthLogin, PermissionResponseMixin, CreateView):
    model = Message
    form_class = MessageForm
    permission_required = "mailing.add_message"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавить новое сообщение для рассылки"
        context["button_text"] = "Добавить"
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("mailing:message_detail", kwargs={"pk": self.object.pk})


class MessageUpdateView(AuthLogin, PermissionResponseMixin, UpdateView):
    model = Message
    form_class = MessageForm
    permission_required = "mailing.change_message"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование сообщения"
        context["button_text"] = "Сохранить изменения"
        return context

    def get_success_url(self):
        return reverse_lazy("mailing:message_detail", kwargs={"pk": self.object.pk})


class MessageDeleteView(AuthLogin, PermissionResponseMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("mailing:message_list")
    permission_required = "mailing.delete_message"

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                request,
                "Невозможно удалить это сообщение, так как оно используется в одной или нескольких рассылках",
            )
            return redirect("mailing:message_list")


class MailingListView(AuthLogin, PermissionResponseMixin, ListView):
    model = Mailing
    paginate_by = 3
    permission_required = "mailing.view_mailing"

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name="manager").exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Список рассылок"
        return context


class MailingDetailView(AuthLogin, PermissionResponseMixin, DetailView):
    model = Mailing
    permission_required = "mailing.view_mailing"

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name="manager").exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=user)


class MailingCreateView(AuthLogin, PermissionResponseMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    permission_required = "mailing.add_message"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавить новую рассылку"
        context["button_text"] = "Добавить"
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("mailing:mailing_detail", kwargs={"pk": self.object.pk})


class MailingUpdateView(AuthLogin, PermissionResponseMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    permission_required = "mailing.change_message"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование рассылки"
        context["button_text"] = "Сохранить изменения"
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy("mailing:mailing_detail", kwargs={"pk": self.object.pk})


class MailingDeleteView(AuthLogin, PermissionResponseMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy("mailing:mailing_list")
    permission_required = "mailing.delete_message"


class MailingToggleActiveView(AuthLogin, PermissionResponseMixin, View):
    permission_required = "mailing.disable_mailing"

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        data = json.loads(request.body)
        mailing.is_active = data["is_active"]
        mailing.save()
        return JsonResponse({"success": True})


class MailingAttemptListView(AuthLogin, ListView):
    model = MailingAttempt
    context_object_name = "mailingattempt_list"
    paginate_by = 10
    ordering = ("-attempt_time",)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Отчет рассылок"
        return context
