from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from .models import EmailVerification
from . import forms
import uuid


def homepage(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = forms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            email_verification = EmailVerification.objects.get(user=user)
            token = email_verification.verification_token

            activation_url = request.build_absolute_uri(
                reverse('activate_account', args=[token])
            )

            email_subject = "Activez votre compte"
            email_body = f"Bonjour {user.username},\n\nCliquez sur le lien pour activer votre compte:\n\n {activation_url}"
            email_from = settings.DEFAULT_FROM_EMAIL
            send_mail(email_subject, email_body, email_from, [user.email], fail_silently=False)

            return redirect('email_confirmation')
        
    else:
        form = forms.CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

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

        email_verification.verification_token = uuid.uuid4()
        email_verification.save()

        activation_url = request.build_absolute_uri(
            reverse('activate_account', args=[email_verification.verification_token])
        )

        email_subject = "Activez votre compte"
        email_body = f"Bonjour {user.username},\n\nCliquez sur le lien pour activer votre compte:\n\n {activation_url}"
        email_from = settings.DEFAULT_FROM_EMAIL
        send_mail(email_subject, email_body, email_from, [user.email], fail_silently=False)
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
                try:
                    email_verification = EmailVerification.objects.get(user=user)
                    if email_verification.verified:
                        login(request, user)
                        return redirect('home')
                    else:
                        messages.error(request, "Vous n'avez pas encore activé votre compte")
                except EmailVerification.DoesNotExist:
                    messages.error(request, "Erreur d'activation du compte. Veuillez vérifier dans vos mails")
            else:
                messages.error(request, "Attention, un des champs rentré n'est pas correct")
    else:
        form = forms.LoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

def confirmation_sent(request):
    return render(request, 'email_confirmation.html')

def activation_failed(request, user_id):
    context = {'user_id': user_id}
    return render(request, 'activation_failed.html', context)

def activation_succeed(request):
    return render(request, 'activation_succeed.html')

def features(request):
    return render(request, 'features.html')

@login_required
def change_email(request):
    if request.method == 'POST':
        form = forms.ChangeEmailForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre mail a bien été modifié, votre mail pour vous connectez sera celui que vous venez de renseigner")
            return redirect('home')
        else:
            return render(request, 'change_email.html', {'form': form})
    else:
        form = forms.ChangeEmailForm(user=request.user)
        return render(request, 'change_email.html', {'form': form})
    
@login_required
def change_password(request):
    if request.method == 'POST':
        form = forms.ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre mot de passe a bien été modifié, votre mot de passe pour vous connectez sera celui que vous venez de renseigner")
            return redirect('home')
        else:
            return render(request, 'change_password.html', {'form': form})
    else:
        form = forms.ChangePasswordForm(user=request.user)
        return render(request, 'change_password.html', {'form': form})
