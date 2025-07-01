from django.urls import path
from .views import (
    ClientListView, ClientDetailView,
    ClientCreateView, ClientUpdateView, ClientDeleteView, ServicePlanCreateView, ServicePlanListView, ServicePlanUpdateView, ServicePlanDeleteView,
    UserGroupCreateView, UserGroupListView, UserGroupUpdateView, UserGroupDeleteView, ClientFilterView
)
from .api_views import service_plans, create_service_plan, user_groups, create_user_group
from .import_csv import import_clients_csv, download_csv, download_sample_csv

urlpatterns = [
    path('', ClientListView.as_view(), name='client_list'),
    path('create/', ClientCreateView.as_view(), name='client_create'),
    path('<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('<int:pk>/edit/', ClientUpdateView.as_view(), name='client_update'),
    path('export/', ClientCreateView.as_view(), name='client_export_csv'), 
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
    path('filter/', ClientFilterView.as_view(), name='client_filter'),
    
    path('import-csv/', import_clients_csv, name='import_clients_csv'),
    path('download-sample-csv/', download_sample_csv, name='download_sample_csv'),
    path('export-clients/', download_csv, name='export_clients_csv'),
    
    path('api/service-plans/', service_plans, name='service_plans'),
    path('api/service-plans/create/', create_service_plan, name='create_service_plan'),
    path('api/user-groups/', user_groups, name='user_groups'),
    path('api/user-groups/create/', create_user_group, name='create_user_group'),
    
    path('service-plans/', ServicePlanListView.as_view(), name='service_plan_list'),
    path('service-plans/create/', ServicePlanCreateView.as_view(), name='service_plan_create'),
    path('service-plans/<int:pk>/edit/', ServicePlanUpdateView.as_view(), name='service_plan_update'),
    path('service-plans/<int:pk>/delete/', ServicePlanDeleteView.as_view(), name='service_plan_delete'),
    
    path('user-groups/', UserGroupListView.as_view(), name='user_group_list'),
    path('user-groups/create/', UserGroupCreateView.as_view(), name='user_group_create'),
    path('user-groups/<int:pk>/edit/', UserGroupUpdateView.as_view(), name='user_group_update'),
    path('user-groups/<int:pk>/delete/', UserGroupDeleteView.as_view(), name='user_group_delete'),

   ] # optional
