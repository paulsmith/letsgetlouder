from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Signee(models.Model):
    user = models.OneToOneField(User)
    signed = models.BooleanField(default=False)
    when = models.DateTimeField(auto_now_add=True)

def sign_pledge(sender, instance, created, **kwargs):
    if created:
        Signee.objects.create(user=instance, signed=True)

post_save.connect(sign_pledge, sender=User)
