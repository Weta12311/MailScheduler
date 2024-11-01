# Generated by Django 5.1.1 on 2024-10-22 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mailing", "0009_alter_mailing_send_time"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="mailing",
            options={
                "ordering": ("-created_at",),
                "permissions": [("disable_mailing", "Может делать рассылку неативной")],
                "verbose_name": "рассылка",
                "verbose_name_plural": "рассылки",
            },
        ),
    ]
