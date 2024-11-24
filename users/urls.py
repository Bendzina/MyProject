from django.urls import path
from . import views
from .views import register_view, CustomLoginView, CustomLogoutView, dashboard_view


app_name = 'users'



urlpatterns = [
    path('', views.dashboard_view, name='dashboard'), 
    path('register/', register_view, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
]