from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from .forms import CustomUserForm
from django.views import View
from django.utils.decorators import method_decorator


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'user_authen/login.html')


@login_required
def home_view(request):
    return render(request, 'user_authen/home.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@method_decorator(login_required, name='dispatch')
class CustomUserListView(View):
    def get(self, request):
        users = CustomUser.objects.all()
        return render(request, 'user_authen/customuser_list.html', {'users': users})

@method_decorator(login_required, name='dispatch')
class CustomUserDetailView(View):
    def get(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        return render(request, 'user_authen/customuser_detail.html', {'user': user})

@method_decorator(login_required, name='dispatch')
class CustomUserCreateView(View):
    def get(self, request):
        form = CustomUserForm()
        return render(request, 'user_authen/customuser_form.html', {'form': form})

    def post(self, request):
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customuser_list')
        return render(request, 'user_authen/customuser_form.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class CustomUserUpdateView(View):
    def get(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        form = CustomUserForm(instance=user)
        return render(request, 'user_authen/customuser_form.html', {'form': form})

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('customuser_detail', pk=pk)
        return render(request, 'user_authen/customuser_form.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class CustomUserDeleteView(View):
    def get(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        return render(request, 'user_authen/customuser_confirm_delete.html', {'user': user})

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        user.delete()
        return redirect('user_authen:customuser_list')