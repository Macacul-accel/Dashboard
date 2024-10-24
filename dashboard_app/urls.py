from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('singup/', views.signup, name='signup'),
    path('activate/<uuid:token>', views.activate_account, name='activate_account'),
    path('email_confirmation/', views.confirmation_sent, name='email_confirmation'),
    path('resend-activation-mail/<int:user_id>', views.resend_activation_email, name='resend_activation_email'),
    path('activation-success/',views.activation_succeed, name='activation_succeed'),
    path('activation-failure/', views.activation_failed, name='activation_failed'),
    path("profile/", views.profile, name="profile"),
    path("settings_profile/", views.settings_profile, name="settings_profile"),
]