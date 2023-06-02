from accounts.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from membership.models import Client, Referral, Student


@receiver(post_save, sender=Student)
def award_referrer_bonus_for_student(sender, instance, created, **kwargs):
    if created:
        referrer_code = instance.referrer_code
        if referrer_code:
            try:
                referring_user = User.objects.get(referral_code=referrer_code)
                referral = Referral(referrer=referring_user, referred_student=instance)
                referral.save()
            except User.DoesNotExist:
                pass


@receiver(post_save, sender=Client)
def award_referrer_bonus_for_client(sender, instance, created, **kwargs):
    if created:
        referrer_code = instance.referrer_code
        if referrer_code:
            try:
                referring_user = User.objects.get(referral_code=referrer_code)
                referral = Referral(referrer=referring_user, referred_client=instance)
                referral.save()
            except User.DoesNotExist:
                pass