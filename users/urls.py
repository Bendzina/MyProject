from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout')
]