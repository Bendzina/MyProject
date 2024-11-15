from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import add_book




urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('', views.book_list, name='book_list'),
    path('add/', add_book, name='add_book')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)