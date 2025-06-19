from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import Client, InternetDetails, InsuranceDetails, TrackingDetails, UploadedDocument, ServicePlan, UserGroup
from .forms import (
    ClientForm, InternetDetailsForm,
    InsuranceDetailsForm, TrackingDetailsForm,
    UploadedDocumentFormSet, AddressForm
)
from django.contrib.auth.mixins import LoginRequiredMixin



class ClientListView(ListView):
    model = Client
    template_name = 'clients/list.html'
    context_object_name = 'clients'


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