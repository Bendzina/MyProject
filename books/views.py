from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Books, Category 
from .forms import BookForm
from django.views.generic import TemplateView, DetailView, FormView
from django.urls import reverse_lazy
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def book_list(request):
    book_list = Books.objects.all().order_by('id')
    paginator = Paginator(book_list, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'book_list.html', {'page_obj': page_obj})

class BooksView(TemplateView):
    template_name = 'book_list.html'

    def get(self, request, *args, **kwargs):
        # Fetch filters from request
        product_name = request.GET.get('q')  # Search query for book title
        category = request.GET.getlist('category')  # Categories selected for filtering

        # Filtering based on search query
        if product_name:
            books = Books.objects.filter(title__icontains=product_name)
        elif category:
            books = Books.objects.filter(category__in=category)
        else:
            books = Books.objects.all()

        # Pagination setup
        paginator = Paginator(books, 10)
        try:
            page_number = request.GET.get('page')
            books_page = paginator.page(page_number)
        except PageNotAnInteger:
            books_page = paginator.page(1)
        except EmptyPage:
            books_page = paginator.page(paginator.num_pages)

        # Get all categories for filtering
        categories = Category.objects.all()
        
        # Prepare context data
        context = {
            'page_obj': books_page,
            'categories': categories,  
        }

        return render(request, self.template_name, context)

def book_detail(request, pk):
    book = get_object_or_404(Books, pk=pk)
    return render(request, 'book_detail.html', {'book': book})

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


def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})

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