from django.urls import path, reverse_lazy
from userauths.views import *
from django.contrib.auth import views as auth_views

app_name = "userauths"

urlpatterns = [
    path("sign-up/", register_view, name="sign-up"),  # URL for the user sign up page
    path("sign-in/", login_view, name="sign-in"),  # URL for the user sign in page
    path("sign-out/", logout_view, name="sign-out"),  # URL for the user sign out
    path('profile/update/', edit_profile, name='edit_profile'),  # URL for the edit profile page
    path('account/change-password/', change_password, name='change-password'),  # URL for the change password page

    # URLs for password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='userauths/forgot-password.html',
        success_url=reverse_lazy('userauths:password_reset_done')
    ), name='password_reset'),

    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='userauths/password-reset-done.html'
    ), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='userauths/password-reset-complete.html'
    ), name='password_reset_complete'),
]
