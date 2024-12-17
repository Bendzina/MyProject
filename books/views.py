from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Books, Category 
from .forms import BookForm
from django.views.generic import TemplateView, DetailView, FormView
from django.urls import reverse_lazy
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def book_list(request):
    query = request.GET.get('q', '').strip()  # Title search
    category = request.GET.get('category', '').strip()  # Selected category

    book_list = Books.objects.all()

    # Apply search filter
    if query:
        book_list = book_list.filter(title__icontains=query)

    # Apply category filter
    if category:
        book_list = book_list.filter(category_id=category)

    paginator = Paginator(book_list, 3)  # Change pagination size as needed
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'book_list.html', {'page_obj': page_obj, 'query': query, 'category': category})


class BooksView(TemplateView):
    template_name = 'book_list.html'

    def get(self, request, *args, **kwargs):
        # Get query parameters
        query = request.GET.get('q', '').strip()  # Search query for book title
        category = request.GET.get('category', '').strip()  # Selected category

        # Base queryset
        books = Books.objects.all()

        # Apply title filter
        if query:
            books = books.filter(title__icontains=query)

        # Apply category filter
        if category:
            books = books.filter(category_id=category)

        # Debugging
        print("Filtered books count:", books.count())
        print("Queryset:", books)

        # Pagination
        paginator = Paginator(books, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Get all categories for dropdown
        all_categories = Category.objects.all()

        # Context
        context = {
            'page_obj': page_obj,
            'categories': all_categories,
            'query': query,
            'selected_category': category,
        }
        return render(request, self.template_name, context)


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




class AddBook(FormView):
    form_class = BookForm
    template_name = 'add_book.html'
    success_url = reverse_lazy('books:book_add')
    def form_valid(self, form):
        books = form.save(commit = False)
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