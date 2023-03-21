from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from server.apps.users import views

app_name = 'users'

auth_urlpatterns = [
    path(
        'auth/login/',
        auth_views.LoginView.as_view(
            template_name='users/auth/login.html',
        ),
        name='login',
    ),
    path(
        'auth/logout/',
        auth_views.LogoutView.as_view(
            template_name='users/auth/logout.html',
        ),
        name='logout',
    ),
    path(
        'auth/password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name='users/auth/password_change.html',
        ),
        name='password_change',
    ),
    path(
        'auth/signup/',
        views.signup,
        name='signup',
    ),
    path(
        'auth/signup/create/',
        views.create_signup,
        name='create_signup',
    ),
    path(
        'auth/activate/done/',
        TemplateView.as_view(
            template_name='users/auth/activate_done.html',
        ),
        name='activate_done',
    ),
    path(
        'auth/activate/<token>/',
        views.activate_user,
        name='activate',
    ),
    path(
        'auth/password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='users/auth/password_change_done.html',
        ),
        name='password_change_done',
    ),
    path(
        'auth/password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='users/auth/password_reset.html',
            email_template_name='users/email/reset.html',
        ),
        name='password_reset',
    ),
    path(
        'auth/password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='users/auth/password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    path(
        'auth/reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='users/auth/password_reset_confirm.html',
        ),
        name='password_reset_confirm',
    ),
    path(
        'auth/reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='users/auth/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),
]

account_urlpatterns = [
    path(
        'users/',
        views.user_list,
        name='list',
    ),
    path(
        'users/<username>/',
        views.user_detail,
        name='detail',
    ),
    path(
        'users/profile/',
        views.profile,
        name='profile',
    ),
    path(
        'users/profile/change/',
        views.change_profile,
        name='change_profile',
    ),
]

urlpatterns = [
    *auth_urlpatterns,
    *account_urlpatterns,
]
