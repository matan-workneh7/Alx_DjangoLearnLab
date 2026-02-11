from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book


class Command(BaseCommand):
    help = 'Create groups and assign permissions for the bookshelf system'

    def handle(self, *args, **options):
        # Create groups
        groups = {
            'Admins': [],
            'Editors': ['can_create', 'can_edit'],
            'Viewers': ['can_view']
        }

        # Get content type for Book model
        book_content_type = ContentType.objects.get_for_model(Book)

        # Get all book permissions
        book_permissions = Permission.objects.filter(
            content_type=book_content_type,
            codename__in=['can_view', 'can_create', 'can_edit', 'can_delete']
        )

        # Create groups and assign permissions
        for group_name, permission_codenames in groups.items():
            group, created = Group.objects.get_or_create(name=group_name)
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created group: {group_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Group {group_name} already exists'))

            # Clear existing permissions
            group.permissions.clear()

            # Assign permissions based on group
            if group_name == 'Admins':
                # Admins get all permissions
                group.permissions.set(book_permissions)
                self.stdout.write(self.style.SUCCESS(f'Assigned all permissions to {group_name}'))
            else:
                # Other groups get specific permissions
                for codename in permission_codenames:
                    try:
                        permission = Permission.objects.get(
                            content_type=book_content_type,
                            codename=codename
                        )
                        group.permissions.add(permission)
                        self.stdout.write(self.style.SUCCESS(f'Assigned {codename} to {group_name}'))
                    except Permission.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f'Permission {codename} not found'))

        self.stdout.write(self.style.SUCCESS('Groups and permissions setup completed!'))
