from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
]

urlpatterns += [
    path('filter/', views.book_filter, name='book_filter'),
    path('add/', views.add_book, name='add_book'),
]
