# Generated by Django 5.1.1 on 2024-10-22 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailing", "0008_client_owner_mailing_owner_message_owner"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailing",
            name="send_time",
            field=models.DateTimeField(verbose_name="дата и время отправки рассылки"),
        ),
    ]