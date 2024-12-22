from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Books, Category 
from .forms import BookForm
from django.views.generic import TemplateView, DetailView, FormView
from django.urls import reverse_lazy
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.permissions import IsAdminUser
from django.core.exceptions import PermissionDenied

class BooksView(TemplateView):
    template_name = 'book_list.html'

    def get(self, request, *args, **kwargs):
        # Get query parameters
        query = request.GET.get('q', '').strip()
        category = request.GET.get('category', '').strip()

        # Base queryset
        books = Books.objects.all()

        # Apply filters
        if query:
            books = books.filter(title__icontains=query)
        if category:
            books = books.filter(category_id=category)

        # Pagination
        paginator = Paginator(books, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Get all categories
        all_categories = Category.objects.all()

        # Context
        context = {
            'page_obj': page_obj,
            'categories': all_categories,
            'query': query,
            'selected_category': category,
        }
        return render(request, 'book_list.html', context)
    
    
class BooksDetailView(DetailView):
    template_name = 'book_detail.html'
    context_object_name = 'book_detail'
    model = Books

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books = self.object
        related_products = Books.objects.filter(category=books.category).exclude(id=books.id)[:4]

        context['related_products'] = related_products
        return context



from django.contrib.auth.mixins import UserPassesTestMixin

# class AddBook(UserPassesTestMixin, FormView):
#     form_class = BookForm
#     template_name = 'add_book.html'
#     success_url = reverse_lazy('books:book_add')

#     # Check if the user is a superadmin
#     def test_func(self):
#         return self.request.user.is_superuser

#     # If the user is not a superadmin, redirect them or show an error
#     def handle_no_permission(self):
#         return render(self.request, '403.html', status=403)

#     def form_valid(self, form):
#         books = form.save(commit=False)
#         books.save()
#         form.save_m2m()
#         return super().form_valid(form)
class AddBook(FormView):
    permission_classes = [IsAdminUser]
    form_class = BookForm
    template_name = 'add_book.html'
    success_url = reverse_lazy('books:book_add')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        books = form.save(commit=False)
        books.save()
        form.save_m2m()
        return super().form_valid(form)



def book_filter(request):
    query = request.GET.get('q')
    if query:
        books = Books.objects.filter(title__icontains=query)
    else:
        books = Books.objects.all()
    return render(request, 'book_list.html', {'books': books})