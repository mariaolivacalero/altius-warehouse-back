# custom_auth/signals.py
# automatically assigns a default group to a newly created user.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from custom_auth.models import User

@receiver(post_save, sender=User)
def assign_default_group(sender, instance, created, **kwargs):
    if created:
        default_group, _ = Group.objects.get_or_create(name='Beneficiaries')
        instance.groups.add(default_group)

