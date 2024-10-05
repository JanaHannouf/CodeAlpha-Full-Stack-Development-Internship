import logging
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from userauths.forms import UserRegisterForm, ProfileForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from userauths.models import User, Profile
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordResetConfirmView

# Create your views here.
def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hello {username}, your account is created successfully!")
            new_user = authenticate(
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password1']                   
            )
            login(request, new_user)
            return redirect("core:index")

    else:
        form = UserRegisterForm()
        

    context = {
        'form': form,
    }
    return render(request, "userauths/sign-up.html", context)

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Hello, you have already logged in!")
        return redirect("core:index")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"You are logged in successfully!")
                return redirect("core:index")
            else:
                messages.warning(request, f"User does not exist, create an account.")
        except:
            messages.warning(request, f"User with the following email address {email} does not exist.")
            
    return render(request, "userauths/sign-in.html")

def logout_view(request):
    logout(request)
    messages.success(request, f"You have logged out.")
    return redirect("userauths:sign-in")

def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            messages.success(request, "Profile is updated successfully.")
            return redirect("core:account")
    else:
        form = ProfileForm(instance=profile)

    context = {
        "form" : form,
        "profile" : profile,
    }
    return render(request, 'userauths/edit-profile.html', context)

@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Your password has been changed successfully.")
            return redirect("core:account-settings")
    else:
        form = PasswordChangeForm(user=request.user)

    context = {
        "form" : form
    }
    return render(request, 'userauths/change-password.html', context)

logger = logging.getLogger(__name__)

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'userauths/password-reset-confirm.html'
    success_url = reverse_lazy('userauths:password_reset_complete')

    def dispatch(self, *args, **kwargs):
        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')
        print(f"Received UID: {uidb64}, Token: {token}")  # Debugging line
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        print("Password change successful!")
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.error("Password change failed: %s", form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['validlink'] = True  # Ensure validlink is set to true
        return context