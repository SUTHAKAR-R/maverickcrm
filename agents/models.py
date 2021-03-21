from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save


class User(AbstractUser):
	is_organizer = models.BooleanField(default=True)
	is_agent = models.BooleanField(default=False)


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.user.username


class Agent(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username


def handler(sender, instance, created, **kwargs):
	if created and instance.is_organizer:
		UserProfile.objects.create(user=instance)

post_save.connect(handler, sender=User)