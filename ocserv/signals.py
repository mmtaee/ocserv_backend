from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from backend.internal.occtl.user import OcctlUser
from ocserv.models import OcservUser


@receiver(post_save, sender=OcservUser)
def add_or_update_ocserv_user(sender, instance, created, **kwargs):
    occtl_user = OcctlUser(username=instance.username)
    group = None if instance.group == "defaults" else instance.group
    if created:
        occtl_user.add_or_update(password=instance.password, group=group)
        if instance.lock:
            occtl_user.lock(lock=True)
    else:
        if update_fields := kwargs.get("update_fields"):
            if "password" in update_fields:
                occtl_user.add_or_update(password=instance.password)
            if "group" in update_fields:
                occtl_user.change_group(group=group)
            if "lock" in update_fields:
                occtl_user.lock(lock=instance.lock)


@receiver(post_delete, sender=OcservUser)
def delete_ocserv_user(sender, instance, **kwargs):
    occtl_user = OcctlUser(username=instance.username)
    occtl_user.delete()
