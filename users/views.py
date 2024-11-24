from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
def register_view(request):
    if request.user.is_authenticated:
        return redirect('users:dashboard')  # თუ მომხმარებელი ავტორიზებულია, გადადის დეშბორდზე
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})



class CustomLoginView(LoginView):
    template_name = 'login.html'

class CustomLogoutView(LogoutView):
    next_page = 'login'

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')


