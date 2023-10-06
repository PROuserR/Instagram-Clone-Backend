from django.urls import path
from .views import *
from rest_framework.authtoken import views

app_name = 'auth'
urlpatterns = [
    path('register_user/', register_user, name='register_user'),
    path('login_user/', views.obtain_auth_token),
    path('generate_token/<str:username>', generate_token, name='generate_token'),
    path('logout_user/', logout_user, name='logout_user'),
    path('user_last_login_update/<int:user_id>', user_last_login_update, name='user_last_login_update'),
    path('update_user/<int:user_id>', update_user, name='update_user'),
    path('update_password/', update_password, name='update_password'),
]