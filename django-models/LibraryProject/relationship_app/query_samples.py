"""
Sample queries for Django relationship models
This script demonstrates queries for Author, Book, Library, and Librarian models
"""

import os
import sys

# Add the project root to Python path for direct execution
sys.path.append('/home/matan/Documents/projects/ALX/Advanced Model Rlsp (Django)/django-models')

# Only setup Django if not already configured
if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
    import django
    django.setup()

from LibraryProject.relationship_app.models import Author, Book, Library, Librarian


def query_books_by_author(author_id):
    """
    Query all books by a specific author
    """
    try:
        author = Author.objects.get(id=author_id)
        books = Book.objects.filter(author=author)
        return books
    except Author.DoesNotExist:
        return []


def list_books_in_library(library_id):
    """
    List all books in a library
    """
    try:
        library = Library.objects.get(id=library_id)
        books = library.books.all()
        return books
    except Library.DoesNotExist:
        return []


def get_librarian_for_library(library_id):
    """
    Retrieve the librarian for a library
    """
    try:
        library = Library.objects.get(id=library_id)
        librarian = Librarian.objects.get(library=library)
        return librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None


if __name__ == "__main__":
    # Example usage (for demonstration purposes)
    print("Query functions defined:")
    print("1. query_books_by_author(author_id) - Query all books by a specific author")
    print("2. list_books_in_library(library_id) - List all books in a library")
    print("3. get_librarian_for_library(library_id) - Retrieve the librarian for a library")