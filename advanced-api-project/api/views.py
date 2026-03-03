from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer


class BookListCreateView(generics.ListCreateAPIView):
    """
    BookListCreateView handles GET (list) and POST (create) operations for Book objects.
    - GET: Returns a paginated list of all books with filtering, searching, and ordering capabilities
    - POST: Creates a new book (requires authentication)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        """
        Custom permission logic:
        - GET requests: Allow any user (read-only access)
        - POST requests: Require authentication
        """
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    # Enable filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title', 'author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['-publication_year', 'title']  # Default ordering


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    BookDetailView handles GET (retrieve), PUT/PATCH (update), and DELETE operations for individual Book objects.
    - GET: Retrieves a single book by ID (read-only access allowed)
    - PUT/PATCH: Updates a book (requires authentication)
    - DELETE: Deletes a book (requires authentication)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        """
        Custom permission logic:
        - GET requests: Allow any user (read-only access)
        - PUT/PATCH/DELETE requests: Require authentication
        """
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class BookUpdateView(generics.UpdateAPIView):
    """
    BookUpdateView handles PUT/PATCH (update) operations for individual Book objects.
    - PUT/PATCH: Updates a book (requires authentication)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """
    BookDeleteView handles DELETE operations for individual Book objects.
    - DELETE: Deletes a book (requires authentication)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class AuthorListView(generics.ListAPIView):
    """
    AuthorListView handles GET operations for Author objects.
    Returns a paginated list of all authors with their nested books.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]  # Read-only access for everyone
    
    # Enable searching and ordering for authors
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']  # Default ordering


class AuthorDetailView(generics.RetrieveAPIView):
    """
    AuthorDetailView handles GET operations for individual Author objects.
    Retrieves a single author by ID with their nested books.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]  # Read-only access for everyone
