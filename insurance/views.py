from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import TravelBookingForm
from .models import TravelBooking
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib import messages
import requests
from django.conf import settings
from django.http import JsonResponse, HttpResponseNotAllowed, Http404
import json 
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime


AUTOMATION_URL = settings.AUTOMATION_SERVICE_URL
INTERNAL_URL = settings.INTERNAL_URL
def upload_photos(request):
    if request.method == 'POST':
        profile_image = request.FILES.get('profile_image')
        passport_image = request.FILES.get('passport_image')
        pdf_file = request.FILES.get('pdf_file')
        if (not profile_image or not passport_image) and not pdf_file:
            messages.warning(request, "Please upload both profile and passport images, or a PDF file.")
        if profile_image and passport_image:
            msg = requests.post(AUTOMATION_URL + '/upload-images/', files={
                'profile_image': profile_image, 'passport_image': passport_image})
            if msg.status_code == 200:
                try:
                    data = msg.json()
                    print(data)
                    passport_data = data.get('passport_data', {})
                    initial_data = {
                        'nationality': passport_data.get('nationality', ''),
                        'surname': passport_data.get('surname', ''),
                        'given_name': passport_data.get('given_name', ''),
                        'dob': passport_data.get('dob', ''),
                        'passport_no': passport_data.get('passport_no', ''),
                        'profile_image_path': data.get('profile_image_url', ''),
                        'passport_image_path': data.get('passport_image_url', ''),
                    }
                    # Store initial data in session and redirect to TravelBookingCreateView
                    request.session['travelbooking_initial'] = initial_data
                    return redirect('insurance:travelbooking_create')
                except Exception as e:
                    messages.error(request, "Failed to process the uploaded PDF. Please try again.")
                messages.success(request, "Images uploaded successfully.")
            else:
                messages.error(request, "Failed to upload images. Please try again.")
        if pdf_file:
            # Send the PDF file to the automation service
            msg = requests.post(AUTOMATION_URL + '/upload_pdf', params={'pdf_file': pdf_file})
            if msg.status_code == 200:
                try:
                    data = msg.json()
                    passport_data = data.get('passport_data', {})
                    initial_data = {
                        'nationality': passport_data.get('nationality', ''),
                        'surname': passport_data.get('surname', ''),
                        'given_name': passport_data.get('given_name', ''),
                        'sex': passport_data.get('sex', ''),
                        'dob': passport_data.get('dob', ''),
                        'passport_no': passport_data.get('passport_no', ''),
                        'profile_image_url': data.get('profile_image_url', ''),
                        'passport_image_url': data.get('passport_image_url', ''),
                    }
                    # Store initial data in session and redirect to TravelBookingCreateView
                    request.session['travelbooking_initial'] = initial_data
                    return redirect('insurance:travelbooking_create')
                except Exception as e:
                    messages.error(request, "Failed to process the uploaded PDF. Please try again.")
            else:
                messages.error(request, "Failed to upload PDF file. Please try again.")
            messages.success(request, "PDF file uploaded successfully.")

    return render(request, 'insurance/upload.html')

class TravelBookingListView(LoginRequiredMixin, ListView):
    model = TravelBooking
    template_name = 'insurance/travelbooking_list.html'
    context_object_name = 'bookings'
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.role == 'admin':
            return TravelBooking.objects.all()
        return TravelBooking.objects.filter(created_by=user)

class TravelBookingDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = TravelBooking
    template_name = 'insurance/travelbooking_detail.html'
    context_object_name = 'booking'

    def test_func(self):
        booking = self.get_object()
        user = self.request.user
        return user.is_superuser or user.role == 'admin' or booking.created_by == user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['show_created_by'] = user.is_superuser or user.role == 'admin'
        return context

def booking_success(request):
    booking = None
    if request.user.is_authenticated:
        booking = TravelBooking.objects.filter(created_by=request.user).order_by('-created_at').first()
    else:
        booking = TravelBooking.objects.order_by('-created_at').first()
    return render(request, 'insurance/success.html', {'booking': booking})

class TravelBookingCreateView(LoginRequiredMixin, CreateView):
    model = TravelBooking
    form_class = TravelBookingForm
    template_name = 'insurance/travelbooking_form.html'
    success_url = reverse_lazy('insurance:travelbooking_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        # Check for initial data in session (set by upload_photos)
        initial_data = self.request.session.pop('travelbooking_initial', None)
        if initial_data:
            kwargs['initial'] = initial_data
        return kwargs

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.created_by = self.request.user
        response = super().form_valid(form)
        # After saving, call the external API with model data
        booking = self.object
        try:
            # Prepare data from the booking instance
            data = {
                "id": str(booking.id),
                "nationality": booking.nationality,
                "travel_from": booking.travel_from,
                "package_id": str(booking.package_id),  # Ensure package_id is str
                "start_date": booking.start_date.strftime('%Y-%m-%d') if isinstance(booking.start_date, datetime) else str(booking.start_date),
                "end_date": booking.end_date.strftime('%Y-%m-%d') if isinstance(booking.end_date, datetime) else str(booking.end_date),
                "surname": booking.surname,
                "given_name": booking.given_name,
                "phone_number": booking.phone_number,
                "email": booking.email,  # Should already be a valid email
                "dob": booking.dob.strftime('%Y-%m-%d') if isinstance(booking.dob, datetime) else str(booking.dob),
                "address": booking.address,
                "emergency_contact": booking.emergency_contact,
                "passport_no": booking.passport_no,
                "profile_image_path": booking.profile_image_path if booking.profile_image_path else None,
                "passport_image_path": booking.passport_image_path if booking.passport_image_path else None,
                "callback_api_url": f"{INTERNAL_URL}/insurance/{booking.id}/is_active/" if booking.id else None
            }
            api_url = AUTOMATION_URL + '/submit-form'
            api_response = requests.post(api_url, json=data)
            if api_response.status_code != 200:
                messages.warning(self.request, "Booking saved, but processing failed.")
        except Exception as e:
            messages.warning(self.request, f"Booking saved, but processing error: {e}")
        return response

class TravelBookingUpdateView(LoginRequiredMixin, UpdateView):
    model = TravelBooking
    form_class = TravelBookingForm
    template_name = 'insurance/travelbooking_form.html'
    success_url = reverse_lazy('insurance:travelbooking_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class TravelBookingDeleteView(LoginRequiredMixin, DeleteView):
    model = TravelBooking
    template_name = 'insurance/travelbooking_confirm_delete.html'
    success_url = reverse_lazy('insurance:travelbooking_list')




@csrf_exempt
def patch_is_active(request, booking_id):
    if request.method != 'PATCH':
        return HttpResponseNotAllowed(['PATCH'])
    try:
        booking = TravelBooking.objects.get(id=booking_id)
    except TravelBooking.DoesNotExist:
        raise Http404("Booking not found")
    try:
        data = json.loads(request.body)
        is_active = data.get('is_active')
        if is_active is not None:
            booking.is_active = bool(is_active)
            booking.save()
            return JsonResponse({'success': True, 'is_active': booking.is_active})
        else:
            return JsonResponse({'success': False, 'error': 'is_active not provided'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
