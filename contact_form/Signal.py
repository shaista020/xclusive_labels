from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import RnDProject, Notification

@receiver(post_save, sender=RnDProject)
def notify_on_rnd_action(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            message=f"New R&D project '{instance.name}' created.",
            user=instance.created_by
        )
