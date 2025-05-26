from django.urls import path
from . import views
from .views import (
    TravelBookingCreateView,
    TravelBookingUpdateView,
    TravelBookingDeleteView,
    # ...other views...
)

app_name = 'insurance'
urlpatterns = [
    path('upload/', views.upload_photos, name='travelbooking_upload'),
    path('success/', views.booking_success, name='booking_success'),
    path('booking-list/', views.TravelBookingListView.as_view(), name='travelbooking_list'),
    path('booking-detail/<int:pk>/', views.TravelBookingDetailView.as_view(), name='travelbooking_detail'),
    path('create/', TravelBookingCreateView.as_view(), name='travelbooking_create'),
    path('<int:pk>/update/', TravelBookingUpdateView.as_view(), name='travelbooking_update'),
    path('<int:pk>/delete/', TravelBookingDeleteView.as_view(), name='travelbooking_delete'),
    path('<int:booking_id>/is_active/', views.patch_is_active, name='patch_is_active'),
]