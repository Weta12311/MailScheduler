from django.urls import path, include

from mailing.views import (
    ClientListView,
    ClientCreateView,
    ClientUpdateView,
    ClientDeleteView,
    ClientDetailView,
    HomePageView,
    MessageListView,
    MessageDetailView,
    MessageCreateView,
    MessageUpdateView,
    MessageDeleteView,
    MailingListView,
    MailingDetailView,
    MailingCreateView,
    MailingUpdateView,
    MailingDeleteView,
    MailingToggleActiveView,
    MailingAttemptListView,
)

app_name = "mailing"

clients_patterns = [
    path("", ClientListView.as_view(), name="client_list"),
    path("<int:pk>/", ClientDetailView.as_view(), name="client_detail"),
    path("create/", ClientCreateView.as_view(), name="client_create"),
    path("edit/<int:pk>/", ClientUpdateView.as_view(), name="client_edit"),
    path("delete/<int:pk>/", ClientDeleteView.as_view(), name="client_delete"),
]

messages_patterns = [
    path("", MessageListView.as_view(), name="message_list"),
    path("<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path("create/", MessageCreateView.as_view(), name="message_create"),
    path("edit/<int:pk>/", MessageUpdateView.as_view(), name="message_edit"),
    path("delete/<int:pk>/", MessageDeleteView.as_view(), name="message_delete"),
]

mailings_patterns = [
    path("", MailingListView.as_view(), name="mailing_list"),
    path("<int:pk>/", MailingDetailView.as_view(), name="mailing_detail"),
    path("create/", MailingCreateView.as_view(), name="mailing_create"),
    path("edit/<int:pk>/", MailingUpdateView.as_view(), name="mailing_edit"),
    path("delete/<int:pk>/", MailingDeleteView.as_view(), name="mailing_delete"),
    path(
        "toggle-active/<int:pk>/",
        MailingToggleActiveView.as_view(),
        name="mailing_toggle_active",
    ),
]

attempts_patterns = [
    path("", MailingAttemptListView.as_view(), name="mailing_attempt_list"),
]

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("clients/", include(clients_patterns)),
    path("messages/", include(messages_patterns)),
    path("mailings/", include(mailings_patterns)),
    path("attempts/", include(attempts_patterns)),
]
