from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('users/list/', views.CustomUserListView.as_view(), name='customuser_list'),
    path('users/create/', views.CustomUserCreateView.as_view(), name='customuser_create'),
    path('users/<int:pk>/', views.CustomUserDetailView.as_view(), name='customuser_detail'),
    path('users/<int:pk>/update/', views.CustomUserUpdateView.as_view(), name='customuser_update'),
    path('users/<int:pk>/delete/', views.CustomUserDeleteView.as_view(), name='customuser_delete'),
]
