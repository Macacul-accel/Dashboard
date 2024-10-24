from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.core.mail import EmailMessage
from django.contrib import messages
from .models import EmailVerification
from . import forms
import uuid


def homepage(request):
    return render(request, 'home')

def signup(request):
    if request.method == 'POST':
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            email_verification = EmailVerification.objects.get(user=user)
            token = email_verification.verifaction_token

            activation_url = request.build_absolute_url(
                reverse('activate_account', args=[token])
            )

            email_subject = "Activez votre compte"
            email_body = f"Bonjour {user.username},\n\nCliquez sur le lien pour activer votre compte:\n\n {activation_url}"
            email = EmailMessage(email_subject, email_body, to=[user.email])
            email.send(fail_silently=False)

            return redirect('email_confirmation')
        
    else:
        form = forms.UserCreationForm()
    return render(request, 'signup', {'form': form})

def activate_account(request, token):
    try:
        email_verification = EmailVerification.objects.get(verification_token=token)
        if email_verification.is_token_expired:
            return render(request, 'activation_failed')

        if not email_verification.verified:
            user = email_verification.user
            user.is_active = True
            user.save()

            email_verification.verified = True
            email_verification.save()

            EmailVerification.objects.filter(user=user).exclude(
                id=email_verification.id
            ).delete()

            return redirect('activation_succeed')
        
    except ObjectDoesNotExist:
        return redirect('activation_failed')
    
def resend_activation_email(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        email_verification = EmailVerification.objects.create(user=user)

        email_verification.verifaction_token = uuid.uuid4()
        email_verification.save()

        activation_url = request.build_absolute_uri(
            reverse('activate_account', args=[email_verification.verifaction_token])
        )

        email_subject = "Activez votre compte"
        email_body = f"Bonjour {user.username},\n\nCliquez sur le lien pour activer votre compte:\n\n {activation_url}"
        email = EmailMessage(email_subject, email_body, to=[user.email])
        email.send(fail_silently=False)
        messages.success("Vérifiez vos mails pour confirmer votre compte")

        return redirect('email_confirmation')
    
    except ObjectDoesNotExist:
        return redirect('activation_failed')

def user_login(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(user)
                return redirect('home')
            else:
                form.add_error(None, "Attention, un des champs rentré n'est pas correct")
    else:
        form = forms.LoginForm()
    return render(request, 'login', {'form': form})

def user_logout(request):
    logout(request)
    messages.success("Vous êtes déconnectés!")
    return redirect('home')

def confirmation_sent(request):
    return render(request, 'email_confirmation')

def activation_failed(request, user_id):
    context = {'user_id': user_id}
    return render(request, 'activation_failed', context)

def activation_succeed(request):
    return render(request, 'activation_succeed')

@login_required
def profile(request):
    user = User.objects.get(id=user.id).username
    return render(request, 'profile', {'username': user})

@login_required
def profile_settings(request):
    return render(request, 'profile_settings')

@login_required
def change_email(request):
    form = forms.ChangeEmailForm()
    if request.method == 'POST':
        form = forms.ChangeEmailForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        return render(request, 'profile_settings', {'form': form})
    
@login_required
def change_password(request):
    form = forms.ChangePasswordForm()
    if request.method == 'POST':
        form = forms.ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        return render(request, 'profile_settings', {'form': form})

