from django.db.models.signals import post_save
from django.dispatch import receiver
from project.models import Activity, Project, Task


@receiver(post_save, sender=Project)
@receiver(post_save, sender=Task)
def create_activity(sender, instance, created, **kwargs):
    if isinstance(instance, Project):
        if created:
            Activity.objects.create(
                user=instance.owner,
                project=instance, 
                task=instance if isinstance(instance, Task) else None,
                activity_type='created_task'
            )
        else:
            Activity.objects.create(
                user=instance.owner,
                project=instance, 
                task=instance if isinstance(instance, Task) else None,
                activity_type='updated_task'
            )
    if isinstance(instance, Task):
        if created:
            Activity.objects.create(
                user=instance.assigned_to,
                project=instance.project, 
                task=instance if isinstance(instance, Task) else None,
                activity_type='created_task'
            )
        else:
            Activity.objects.create(
                user=instance.assigned_to,
                project=instance.project, 
                task=instance if isinstance(instance, Task) else None,
                activity_type='updated_task'
            )
