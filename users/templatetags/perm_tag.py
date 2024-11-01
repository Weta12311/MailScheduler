from django import template

register = template.Library()


@register.filter
def manager_superuser_only(user):
    return user.is_superuser or user.groups.filter(name="manager").exists()


@register.filter
def regular_user_only(user):
    return user.is_superuser or user.groups.filter(name="regular_user").exists()
