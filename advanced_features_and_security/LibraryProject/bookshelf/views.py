from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from .models import Book
from .forms import ExampleForm
from .forms import BookForm

@login_required
def book_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        books = Book.objects.filter(
            Q(title__icontains=search_query) | 
            Q(author__name__icontains=search_query)
        )
    else:
        books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})
