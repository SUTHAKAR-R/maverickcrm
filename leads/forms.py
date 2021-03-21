from django import forms
from .models import Lead, Category
from agents.models import Agent

class LeadForm(forms.ModelForm):
	class Meta:
		model = Lead
		fields = '__all__'

class AssignAgentForm(forms.Form):
	agent = forms.ModelChoiceField(queryset=Agent.objects.all())

	def __init__(self, *args, **kwargs):
		request = kwargs.pop('request')
		agents = Agent.objects.filter(organization=request.user.userprofile)
		super().__init__(*args, **kwargs)
		self.fields['agent'].queryset = agents

class CategoryUpdateForm(forms.ModelForm):
	class Meta:
		model = Lead
		fields = ('category',)