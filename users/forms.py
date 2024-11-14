import re
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import EmailVerification
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):

    username = forms.CharField(
        required=True,
        )
    
    email = forms.EmailField(
        widget=forms.EmailInput,
        required=True,
        )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        required=True
        )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    #So there is no 2 users with the same username or the same email
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            self.add_error('username', "Ce nom d'utilisateur existe déjà")

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            self.add_error('email', "Cette adresse mail existe déjà")
        
        return email

    #The password should contain at least one uppercase letter, one lowercase letter and one digit
    def clean_password(self):
        password = self.cleaned_data.get('password1')
        password_regex = re.compile(r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$")

        if len(password) < 8:
            self.add_error('password1', "Votre MDP doit contenir au minimum 8 caractères.")
        
        if not password_regex.match(password):
            self.add_error('password1',
            "Votre MDP doit contenir au moins une lettre majuscule, une lettre minuscule ainsi qu'un chiffre."
            )
        
        return password
    
    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        
        if commit:
            user.save()
            EmailVerification.objects.create(user=user)

        return user
    

#The user can login with his email
class LoginForm(forms.Form):

    email = forms.CharField(
        required=True,
        widget=forms.EmailInput
        )
    
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput
        )


class ChangeEmailForm(forms.Form):

    error_messages = {
        'email_mismatch': _("Les deux adresses mail rentrées ne sont pas similaires."),
        'not_changed': _("Veuillez rentrer une nouvelle adresse mail."),
    }

    new_email1 = forms.EmailField(
        label=_('Nouvelle adresse mail'),
        widget=forms.EmailInput,
        required=True
        )
    
    new_email2 = forms.EmailField(
        label=_('Confirmation de la nouvelle adresse mail'),
        widget=forms.EmailInput,
        required=True
        )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangeEmailForm, self).__init__(*args, **kwargs)
    
    def clean_new_email1(self):
        old_email = self.user.email
        new_email1 = self.cleaned_data.get('new_email1')

        if old_email and new_email1:
            if old_email == new_email1:
                raise forms.ValidationError(
                    self.error_messages['not_changed'],
                    code='not_changed',
                    )
            return new_email1
        
    def clean_new_email2(self):
        new_email1 = self.cleaned_data.get('new_email1')
        new_email2 = self.cleaned_data.get('new_email2')

        if new_email1 and new_email2:
            if new_email1 != new_email2:
                raise forms.ValidationError(
                    self.error_messages['email_mismatch'],
                    code='email_mismatch',
                    )
            return new_email2
    
    def save(self, commit=True):
        email = self.cleaned_data['new_email1']
        self.user.email = email
        if commit:
            self.user.save()
        return self.user

class ChangePasswordForm(forms.Form):

    error_messages = {
        'password_mismatched' : _("Les deux mots de passe rentrés ne sont pas similaires"),
        'psswd_not_changed' : _("Veuillez rentrer un nouveau mot de passe"),
    }

    new_password1 = forms.CharField(
        label='Nouveau mot de passe',
        widget=forms.PasswordInput,
        required=True
        )
    
    new_password2 = forms.CharField(
        label='Confirmation du nouveau mot de passe',
        widget=forms.PasswordInput,
        required=True
        )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password1(self):
        old_password = self.user.password
        new_password1 = self.cleaned_data.get('new_password1')

        if old_password and new_password1:
            if old_password == new_password1:
                raise forms.ValidationError(
                    self.error_messages['psswd_not_changed'],
                    code='psswd_not_changed',
                    )
            return new_password1
        
    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')

        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatched'],
                    code='password_mismatched'
                )
            return new_password2
        
    def save(self, commit=True):
        password = self.cleaned_data['new_password1']
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


#class RecoverPasswordForm(forms.Form):
