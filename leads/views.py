from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse
from django.core.mail import send_mail
from .models import Lead, Category
from .forms import LeadForm, AssignAgentForm, CategoryUpdateForm
from agents.mixins import OrganizerAndLoginRequiredMixin


class LandingView(generic.TemplateView):
    template_name = "landing.html"

	
class LeadListView(LoginRequiredMixin, generic.ListView):
	template_name = 'leads/lead_list.html'
	context_object_name = 'leads'

	def get_queryset(self):
		user = self.request.user
		if user.is_organizer:
			queryset = Lead.objects.filter(organization=user.userprofile, agent__isnull=False)
		else:
			queryset = Lead.objects.filter(organization=user.agent.organization, agent__isnull=False)
			queryset = queryset.filter(agent__user=self.request.user)
		return queryset

	def get_context_data(self, **kwargs):
		user = self.request.user
		context = super().get_context_data(**kwargs)
		if user.is_organizer:
			context["unassigned_leads"] = Lead.objects.filter(organization=user.userprofile, agent__isnull=True)
		return context
	
	
class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    model = Lead
    template_name = "leads/lead_detail.html"
    context_object_name = "lead"


class LeadCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
	form_class = LeadForm
	template_name = "leads/lead_create.html"

	def get_success_url(self):
		return reverse('lead_list')

	def form_valid(self, form):
		send_mail(
			subject='A lead has been created',
			message='Go to the site to see th lead',
			from_email='test@test.com',
			recipient_list=['test1@test.com'],
		)
		return super().form_valid(form)


class LeadUpdateView(LoginRequiredMixin, generic.UpdateView):
	template_name = 'leads/lead_update.html'
	form_class = LeadForm
	
	def get_success_url(self):
		return reverse('lead_list')

	def get_queryset(self):
		return Lead.objects.filter(organization=self.request.user.userprofile)


class LeadDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
    model = Lead
    template_name = "leads/lead_delete.html"

    def get_success_url(self):
        return reverse('lead_list')


class AssignAgentView(OrganizerAndLoginRequiredMixin, generic.FormView):
	template_name = 'leads/assign_agent.html'
	form_class = AssignAgentForm
	
	def get_success_url(self):
		return reverse('lead_list')

	def get_form_kwargs(self, **kwargs):
		kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
		kwargs['request'] = self.request
		return kwargs

	def form_valid(self, form):
		agent = form.cleaned_data['agent']
		print(agent)
		lead = Lead.objects.get(id=self.kwargs['pk'])
		lead.agent = agent
		lead.save()
		return super(AssignAgentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, generic.ListView):
	template_name = 'leads/category_list.html'
	context_object_name = 'categories'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = self.request.user
		if user.is_organizer:
			queryset = Lead.objects.filter(organization=user.userprofile)
		else:
			queryset = Lead.objects.filter(organization=user.agent.userprofile)
		context["unassigned_lead_count"] = queryset.filter(category__isnull=True).count()
		return context
	

	def get_queryset(self):
		user = self.request.user
		if user.is_organizer:
			queryset = Category.objects.filter(organization=user.userprofile)
		else:
			queryset = Category.objects.filter(organization=user.agent.userprofile)
		return queryset


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
	template_name = 'leads/category_detail.html'
	context_object_name = 'category'

	def get_context_data(self, **kwargs):
		user = self.request.user
		context = super().get_context_data(**kwargs)
		context["leads"] = Lead.objects.filter(category=self.get_object())
		return context
	

	def get_queryset(self):
		user = self.request.user
		if user.is_organizer:
			queryset = Category.objects.filter(organization=user.userprofile)
		else:
			queryset = Category.objects.filter(organization=user.agent.userprofile)
		return queryset


class CategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
	form_class = CategoryUpdateForm
	template_name = "leads/category_update.html"

	def get_success_url(self):
		return reverse('lead_detail', kwargs={"pk" : self.get_object().id})

	def get_queryset(self):
		user = self.request.user
		if user.is_organizer:
			queryset = Lead.objects.filter(organization=user.userprofile)
		else:
			queryset = Lead.objects.filter(organization=user.agent.userprofile)
		return queryset
	
