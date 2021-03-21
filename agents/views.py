from django.shortcuts import reverse
from django.views import generic
from django.core.mail import send_mail
from random import randint
from .models import Agent
from .forms import CustomUserCreationForm, AgentForm
from .mixins import OrganizerAndLoginRequiredMixin

class SignupView(generic.CreateView):
	form_class = CustomUserCreationForm
	template_name = 'registration/signup.html'

	def get_success_url(self):
		return reverse('lead_list')


class AgentListView(OrganizerAndLoginRequiredMixin, generic.ListView):
	template_name = 'agents/agent_list.html'
	context_object_name = 'agents'

	def get_queryset(self):
		organization = self.request.user.userprofile
		return Agent.objects.filter(organization=organization)
	

class AgentCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
	form_class = AgentForm
	template_name = "agents/agent_create.html"

	def get_success_url(self):
		return reverse('agent_list')

	def form_valid(self, form):
		user = form.save(commit=False)
		user.is_organizer = False
		user.is_agent = True
		user.set_password(f'{randint(0, 1000000)}')
		user.save()
		Agent.objects.create(user=user, organization=self.request.user.userprofile)
		send_mail(
			subject='Agent Invitation',
			message='You have been invited to be an agent',
			from_email='admin@info.com',
			recipient_list=['agent@email.com',]
		)
		return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganizerAndLoginRequiredMixin, generic.DetailView):
	model = Agent
	template_name = "agents/agent_detail.html"
	context_object_name = 'agent'


class AgentUpdateView(OrganizerAndLoginRequiredMixin, generic.UpdateView):
	template_name = "agents/agent_update.html"
	form_class = AgentForm

	def get_success_url(self):
		return reverse('agent_list')

	def get_queryset(self):
		organization = self.request.user.userprofile
		return Agent.objects.filter(organization=organization)


class AgentDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
	model = Agent
	template_name = "agents/agent_delete.html"

	def get_success_url(self):
		return reverse('agent_list')