from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import Client, InternetDetails, InsuranceDetails, TrackingDetails, UploadedDocument, ServicePlan, UserGroup
from .forms import (
    ClientFilterForm, ClientForm, InternetDetailsForm,
    InsuranceDetailsForm, ServicePlanForm, TrackingDetailsForm,
    UploadedDocumentFormSet, AddressForm, UserGroupForm
)

from django.views.generic.edit import FormView
from django.urls import reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

class UserGroupListView(ListView):
    model = UserGroup
    template_name = 'usergroup/list.html'
    context_object_name = 'user_groups'
    
class ServicePlanListView(ListView):
    model = ServicePlan
    template_name = 'serviceplan/list.html'
    context_object_name = 'service_plans'
    
class UserGroupUpdateView(UpdateView):
    model = UserGroup
    form_class = UserGroupForm
    template_name = 'usergroup/form.html'
    success_url = reverse_lazy('user_group_list')
    
class ServicePlanUpdateView(UpdateView):
    model = ServicePlan
    form_class = ServicePlanForm
    template_name = 'serviceplan/form.html'
    success_url = reverse_lazy('service_plan_list')
    
class UserGroupCreateView(CreateView):
    model = UserGroup
    form_class = UserGroupForm
    template_name = 'usergroup/form.html'
    success_url = reverse_lazy('user_group_list')
    
class ServicePlanCreateView(CreateView):
    model = ServicePlan
    form_class = ServicePlanForm
    template_name = 'serviceplan/form.html'
    success_url = reverse_lazy('service_plan_list')
    
class UserGroupDeleteView(LoginRequiredMixin, DeleteView):
    model = UserGroup
    template_name = 'usergroup/confirm_delete.html'
    success_url = reverse_lazy('user_group_list')

    def get_queryset(self):
        # Optionally restrict deletion to only objects the user owns (if you have such logic)
        return UserGroup.objects.all()

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().delete(request, *args, **kwargs)
    
class ServicePlanDeleteView(LoginRequiredMixin, DeleteView):
    model = ServicePlan
    template_name = 'serviceplan/confirm_delete.html'
    success_url = reverse_lazy('service_plan_list')

    def get_queryset(self):
        # Optionally restrict deletion to only objects the user owns (if you have such logic)
        return ServicePlan.objects.all()

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().delete(request, *args, **kwargs)

class ClientListView(ListView):
    model = Client
    template_name = 'clients/list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        queryset = super().get_queryset()
        # Main client fields
        first_name = self.request.GET.get('first_name', '')
        last_name = self.request.GET.get('last_name', '')
        email = self.request.GET.get('email', '')
        phone_number = self.request.GET.get('phone_number', '')
        vat_pan = self.request.GET.get('vat_pan', '')
        company_name = self.request.GET.get('company_name', '')
        # Address fields
        city = self.request.GET.get('city', '')
        province = self.request.GET.get('province', '')
        # InternetDetails fields
        username_or_mac = self.request.GET.get('username_or_mac', '')
        service_plan = self.request.GET.get('service_plan', '')
        user_group = self.request.GET.get('user_group', '')
        # InsuranceDetails fields
        insurance_comments = self.request.GET.get('insurance_comments', '')
        # TrackingDetails fields
        travel_from = self.request.GET.get('travel_from', '')
        package = self.request.GET.get('package', '')
        # General search
        search = self.request.GET.get('search', '')

        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)
        if email:
            queryset = queryset.filter(email__icontains=email)
        if phone_number:
            queryset = queryset.filter(phone_number__icontains=phone_number)
        if vat_pan:
            queryset = queryset.filter(vat_pan__icontains=vat_pan)
        if company_name:
            queryset = queryset.filter(company_name__icontains=company_name)
        if city:
            queryset = queryset.filter(address__city__icontains=city)
        if province:
            queryset = queryset.filter(address__province__icontains=province)
        if username_or_mac:
            queryset = queryset.filter(internetdetails__username_or_mac__icontains=username_or_mac)
        if service_plan:
            queryset = queryset.filter(internetdetails__service_plan__id=service_plan)
        if user_group:
            queryset = queryset.filter(internetdetails__user_group__id=user_group)
        if insurance_comments:
            queryset = queryset.filter(insurancedetails__insurance_comments__icontains=insurance_comments)
        if travel_from:
            queryset = queryset.filter(trackingdetails__travel_from__icontains=travel_from)
        if package:
            queryset = queryset.filter(trackingdetails__package__icontains=package)
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(phone_number__icontains=search) |
                Q(company_name__icontains=search) |
                Q(address__city__icontains=search) |
                Q(address__province__icontains=search) |
                Q(internetdetails__username_or_mac__icontains=search) |
                Q(internetdetails__service_plan__name__icontains=search) |
                Q(internetdetails__user_group__name__icontains=search) |
                Q(insurancedetails__insurance_comments__icontains=search) |
                Q(trackingdetails__travel_from__icontains=search) |
                Q(trackingdetails__package__icontains=search)
            ).distinct()
        return queryset


class ClientDetailView(DetailView):
    model = Client
    template_name = 'clients/detail.html'
    context_object_name = 'client'

class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'clients/confirm_delete.html'
    success_url = reverse_lazy('client_list')

    def get_queryset(self):
        # Optionally restrict deletion to only objects the user owns (if you have such logic)
        return Client.objects.all()

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().delete(request, *args, **kwargs)

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/form.html'
    success_url = reverse_lazy('client_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['address_form'] = AddressForm(self.request.POST or None, prefix='address')
        context['perma_address_form'] = AddressForm(self.request.POST or None, prefix='perma')

        if self.request.POST:
            context['internet_form'] = InternetDetailsForm(self.request.POST)
            context['insurance_form'] = InsuranceDetailsForm(self.request.POST)
            context['tracking_form'] = TrackingDetailsForm(self.request.POST)
            context['document_formset'] = UploadedDocumentFormSet(self.request.POST, self.request.FILES)
        else:
            context['internet_form'] = InternetDetailsForm()
            context['insurance_form'] = InsuranceDetailsForm()
            context['tracking_form'] = TrackingDetailsForm()
            context['document_formset'] = UploadedDocumentFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        internet_form = context['internet_form']
        insurance_form = context['insurance_form']
        tracking_form = context['tracking_form']
        document_formset = context['document_formset']
        address_form = context['address_form']
        perma_address_form = context['perma_address_form']
        same_address = self.request.POST.get("same_address") == "on"

        # Save the main Client form (mandatory)
        if not (address_form.is_valid() and (perma_address_form.is_valid() or same_address)):
            return self.form_invalid(form)

        address = address_form.save()

        if same_address:
            perma_address = address
        else:
            perma_address = perma_address_form.save()

        self.object = form.save(commit=False)
        self.object.address = address
        self.object.perma_address = perma_address
        self.object.created_by = self.request.user
        self.object.agent = self.request.user
        self.object.save()

        # Check if InternetDetails form has data and is valid
        if internet_form.has_changed() and internet_form.is_valid():
            internet = internet_form.save(commit=False)
            internet.customer = self.object
            internet.save()

        # Check if InsuranceDetails form has data and is valid
        if insurance_form.has_changed() and insurance_form.is_valid():
            insurance = insurance_form.save(commit=False)
            insurance.customer = self.object
            insurance.save()

        # Check if TrackingDetails form has data and is valid
        if tracking_form.has_changed() and tracking_form.is_valid():
            tracking = tracking_form.save(commit=False)
            tracking.customer = self.object
            tracking.save()

        # Check if DocumentFormSet has data and is valid
        if document_formset.has_changed() and document_formset.is_valid():
            document_formset.instance = self.object
            document_formset.save()

        return redirect(self.success_url)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/form.html'
    success_url = reverse_lazy('client_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['address_form'] = AddressForm(self.request.POST or None, prefix='address')
        context['perma_address_form'] = AddressForm(self.request.POST or None, prefix='perma')
        if self.request.POST:
            context['internet_form'] = InternetDetailsForm(self.request.POST, instance=self.object.internetdetails if hasattr(self.object, 'internetdetails') else None)
            context['insurance_form'] = InsuranceDetailsForm(self.request.POST, instance=self.object.insurancedetails if hasattr(self.object, 'insurancedetails') else None)
            context['tracking_form'] = TrackingDetailsForm(self.request.POST, instance=self.object.trackingdetails if hasattr(self.object, 'trackingdetails') else None)
            context['document_formset'] = UploadedDocumentFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['address_form'] = AddressForm(prefix='address', instance=self.object.address)
            context['perma_address_form'] = AddressForm(prefix='perma', instance=self.object.perma_address)
            context['internet_form'] = InternetDetailsForm(instance=self.object.internetdetails if hasattr(self.object, 'internetdetails') else None)
            context['insurance_form'] = InsuranceDetailsForm(instance=self.object.insurancedetails if hasattr(self.object, 'insurancedetails') else None)
            context['tracking_form'] = TrackingDetailsForm(instance=self.object.trackingdetails if hasattr(self.object, 'trackingdetails') else None)
            context['document_formset'] = UploadedDocumentFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        internet_form = context['internet_form']
        insurance_form = context['insurance_form']
        tracking_form = context['tracking_form']
        document_formset = context['document_formset']
        address_form = context['address_form']
        perma_address_form = context['perma_address_form']
        same_address = self.request.POST.get("same_address") == "on"

        # Save the main Client form (mandatory)
        if not (address_form.is_valid() and (perma_address_form.is_valid() or same_address)):
            return self.form_invalid(form)

        address = address_form.save()

        if same_address:
            perma_address = address
        else:
            perma_address = perma_address_form.save()

        self.object = form.save(commit=False)
        self.object.address = address
        self.object.perma_address = perma_address
        self.object.save()


        # Save the main Client form (mandatory)
        self.object = form.save()

        # Check if InternetDetails form has data and is valid
        if internet_form.has_changed() and internet_form.is_valid():
            internet = internet_form.save(commit=False)
            internet.customer = self.object
            internet.save()

        # Check if InsuranceDetails form has data and is valid
        if insurance_form.has_changed() and insurance_form.is_valid():
            insurance = insurance_form.save(commit=False)
            insurance.customer = self.object
            insurance.save()

        # Check if TrackingDetails form has data and is valid
        if tracking_form.has_changed() and tracking_form.is_valid():
            tracking = tracking_form.save(commit=False)
            tracking.customer = self.object
            tracking.save()

        # Check if DocumentFormSet has data and is valid
        if document_formset.has_changed() and document_formset.is_valid():
            document_formset.instance = self.object
            document_formset.save()

        return redirect(self.success_url)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))



class ClientFilterView(FormView):
    template_name = 'clients/filter.html'
    form_class = ClientFilterForm

    def form_valid(self, form):
        # Build query params from form data
        data = {k: v for k, v in form.cleaned_data.items() if v not in [None, '', 0]}
        query_string = "&".join([f"{k}={v}" for k, v in data.items()])
        url = reverse('client_list')  # Ensure this matches the name in your urls.py for ClientListView
        if query_string:
            url = f"{url}?{query_string}"
        return redirect(url)

    def get_initial(self):
        # Prepopulate form with GET params if present
        return self.request.GET.dict()