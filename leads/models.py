from django.db import models
from django.utils import timezone
from agents.models import Agent, UserProfile


class Category(models.Model):
	name = models.CharField(max_length=20)
	organization = models.ForeignKey(UserProfile, related_name='leads', on_delete=models.CASCADE)

	class Meta:
		verbose_name = "Category"
		verbose_name_plural = "Categories"

	def __str__(self):
		return self.name

	
class Lead(models.Model):
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	age = models.IntegerField(default=0)
	organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	agent = models.ForeignKey(Agent, null=True, blank=True,  on_delete=models.SET_NULL)
	category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
	description = models.TextField()
	date_added = models.DateTimeField(auto_now_add=timezone.now)
	phone_number = models.CharField(max_length=20)
	email = models.EmailField()

	def __str__(self):
		return f'{self.first_name} {self.last_name}'
		