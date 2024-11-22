from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Books
from .forms import BookForm

def book_list(request):
    book_list = Books.objects.all().order_by('id')
    paginator = Paginator(book_list, 10)  # 10 წიგნი თითო გვერდზე
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'book_list.html', {'page_obj': page_obj})

def book_detail(request, pk):
    book = get_object_or_404(Books, pk=pk)
    return render(request, 'book_detail.html', {'book': book})

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})

def book_filter(request):
    query = request.GET.get('q')
    if query:
        books = Books.objects.filter(title__icontains=query)
    else:
        books = Books.objects.all()
    return render(request, 'book_list.html', {'books': books})