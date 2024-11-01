from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        groups_permissions = {
            'regular_user': [
                'mailing.add_client',
                'mailing.change_client',
                'mailing.delete_client',
                'mailing.view_client',
                
                'mailing.add_mailing',
                'mailing.change_mailing',
                'mailing.delete_mailing',
                'mailing.view_mailing',

                'mailing.view_mailingattempt',

                'mailing.add_message',
                'mailing.change_message',
                'mailing.delete_message',
                'mailing.view_message'
            ],
            'manager': [
                'mailing.view_mailingattempt',
                'mailing.view_mailing',
                "mailing.disable_mailing",

                'users.block_users',
                'users.view_user'
            ],
            'content_manager': [
                'blog.add_article',
                'blog.change_article',
                'blog.delete_article',
                'blog.view_article'
            ],
        }

        for group_name, permissions in groups_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)

            for perm in permissions:
                try:
                    permission = Permission.objects.get(codename=perm.split('.')[1],
                                                        content_type__app_label=perm.split('.')[0])
                    group.permissions.add(permission)
                    self.stdout.write(self.style.SUCCESS(f'Добавлено право: {perm} в группу {group_name}'))
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Право {perm} не найдено для группы {group_name}.'))

            group.save()
            self.stdout.write(self.style.SUCCESS(f'Группа {group_name} обновлена с правами.'))

