from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    email = models.EmailField(unique=True)

    # Override the groups field
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="custom_user_set",
        related_query_name="custom_user",
    )

    # Override the user_permissions field
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="custom_user_set",
        related_query_name="custom_user",
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']