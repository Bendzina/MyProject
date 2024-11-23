from django.urls import path
from . import views
from .views import register_view
from .views import CustomLoginView, CustomLogoutView




urlpatterns =[
    path('register/', register_view, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

]