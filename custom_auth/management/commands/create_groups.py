# custom_auth/management/commands/create_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from custom_auth.models import User

class Command(BaseCommand):
    help = 'Create initial groups and assign permissions'

    def handle(self, *args, **kwargs):
        # Define group names
        groups = ['Beneficiaries', 'Food Bank Staff', 'Volunteers', 'System Administrators']
        
        # Create groups and assign permissions
        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Group "{group_name}" created'))
            else:
                self.stdout.write(self.style.WARNING(f'Group "{group_name}" already exists'))

        # Assign permissions (example permissions)
        self.assign_permissions()

    def assign_permissions(self):
        # Beneficiaries permissions
        beneficiaries_permissions = [
            # Add specific permissions
        ]
        self.add_permissions_to_group('Beneficiaries', beneficiaries_permissions)

        # Food Bank Staff permissions
        staff_permissions = [
            'add_item', 'change_item', 'delete_item', 'view_item',  # Example model permissions
            # Add more specific permissions
        ]
        self.add_permissions_to_group('Food Bank Staff', staff_permissions)

        # Volunteers permissions
        volunteers_permissions = [
            'view_item',  # Example model permissions
            # Add more specific permissions
        ]
        self.add_permissions_to_group('Volunteers', volunteers_permissions)

        # System Administrators permissions
        admin_permissions = Permission.objects.all()  # Give all permissions
        self.add_permissions_to_group('System Administrators', admin_permissions)

    def add_permissions_to_group(self, group_name, permissions):
        group = Group.objects.get(name=group_name)
        if isinstance(permissions, list):
            for perm in permissions:
                permission = Permission.objects.get(codename=perm)
                group.permissions.add(permission)
        else:
            group.permissions.set(permissions)
        group.save()

        self.stdout.write(self.style.SUCCESS(f'Permissions assigned to "{group_name}"'))


