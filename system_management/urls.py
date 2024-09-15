# system_management/urls.py
from django.urls import path
from system_management import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('login/', views.login_view, name='login'),
    path('signup/', views.register_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_page, name='home'),
    path('profile/', views.profile_view, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('view_users/', views.view_users, name='view_users'),
    path('add_user/', views.add_user, name='add_user'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        html_email_template_name='registration/password_reset_email.html'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('change_user_status/<int:user_id>/', views.change_user_status, name='toggle_user_status'),
    path('update_user/<int:user_id>/', views.update_user, name='update_user'),
   
]