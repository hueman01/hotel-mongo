from django.apps import apps
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    app_config = apps.get_app_config('TipoHabitacion')
    if sender.label != app_config.label:
        return

    models = app_config.get_models()
    admin_group, _ = Group.objects.get_or_create(name='Administradores')
    client_group, _ = Group.objects.get_or_create(name='Clientes')

    admin_permissions = []
    view_permissions = []
    for model in models:
        meta = model._meta
        for action in ('view', 'add', 'change', 'delete'):
            permission = Permission.objects.get(
                content_type__app_label=meta.app_label,
                codename=f'{action}_{meta.model_name}',
            )
            admin_permissions.append(permission)
            if action == 'view':
                view_permissions.append(permission)

    admin_group.permissions.set(admin_permissions)
    client_group.permissions.set(view_permissions)
