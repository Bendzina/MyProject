from django.urls import path
from . import views 
from .views import BooksView, BooksDetailView, AddBook

app_name = 'books'

urlpatterns = [
    # path('', views.book_list, name='book_list'),
    path('', BooksView.as_view(), name='book_list'),
    # path('books/', views.BooksView.as_view(), name='books_view'),
    # path('book/detail/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/<int:pk>/', views.BooksDetailView.as_view(), name='book_detail'),
    # path('book/<int:pk>/edit/', views.BookUpdateView.as_view(), name='book_edit'),
]

urlpatterns += [
    path('filter/', views.book_filter, name='book_filter'),
    # path('add/', views.add_book, name='add_book'),
    path('add/', views.AddBook.as_view(), name='book_add'),
]
