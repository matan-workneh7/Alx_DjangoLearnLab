"""
Test script for query_samples.py functions
Creates sample data and tests all query functions
"""

import os
import sys
import django

# Add the project root to Python path
sys.path.append('/home/matan/Documents/projects/ALX/Advanced Model Rlsp (Django)/django-models')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from LibraryProject.relationship_app.models import Author, Book, Library, Librarian
from LibraryProject.relationship_app.query_samples import query_books_by_author, list_books_in_library, get_librarian_for_library


def create_sample_data():
    """Create sample data for testing"""
    print("Creating sample data...")
    
    # Create authors
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George Orwell")
    
    # Create books
    book1 = Book.objects.create(title="Harry Potter", author=author1)
    book2 = Book.objects.create(title="1984", author=author2)
    book3 = Book.objects.create(title="Animal Farm", author=author2)
    
    # Create libraries
    library1 = Library.objects.create(name="Central Library")
    library2 = Library.objects.create(name="Community Library")
    
    # Add books to libraries
    library1.books.add(book1, book2)
    library2.books.add(book3)
    
    # Create librarians
    librarian1 = Librarian.objects.create(name="John Smith", library=library1)
    librarian2 = Librarian.objects.create(name="Jane Doe", library=library2)
    
    print("Sample data created successfully!")
    return {
        'author1': author1,
        'author2': author2,
        'book1': book1,
        'book2': book2,
        'book3': book3,
        'library1': library1,
        'library2': library2,
        'librarian1': librarian1,
        'librarian2': librarian2
    }


def test_query_functions(data):
    """Test all query functions"""
    print("\n" + "="*50)
    print("TESTING QUERY FUNCTIONS")
    print("="*50)
    
    # Test 1: query_books_by_author
    print("\n1. Testing query_books_by_author:")
    books_by_author1 = query_books_by_author(data['author1'].id)
    print(f"   Books by {data['author1'].name}: {[book.title for book in books_by_author1]}")
    
    books_by_author2 = query_books_by_author(data['author2'].id)
    print(f"   Books by {data['author2'].name}: {[book.title for book in books_by_author2]}")
    
    # Test 2: list_books_in_library
    print("\n2. Testing list_books_in_library:")
    books_in_lib1 = list_books_in_library(data['library1'].id)
    print(f"   Books in {data['library1'].name}: {[book.title for book in books_in_lib1]}")
    
    books_in_lib2 = list_books_in_library(data['library2'].id)
    print(f"   Books in {data['library2'].name}: {[book.title for book in books_in_lib2]}")
    
    # Test 3: get_librarian_for_library
    print("\n3. Testing get_librarian_for_library:")
    librarian1 = get_librarian_for_library(data['library1'].id)
    print(f"   Librarian for {data['library1'].name}: {librarian1.name if librarian1 else 'None'}")
    
    librarian2 = get_librarian_for_library(data['library2'].id)
    print(f"   Librarian for {data['library2'].name}: {librarian2.name if librarian2 else 'None'}")
    
    # Test edge cases
    print("\n4. Testing edge cases:")
    
    # Non-existent author
    books_by_nonexistent = query_books_by_author(999)
    print(f"   Books by non-existent author: {books_by_nonexistent}")
    
    # Non-existent library
    books_in_nonexistent = list_books_in_library(999)
    print(f"   Books in non-existent library: {books_in_nonexistent}")
    
    # Non-existent librarian
    librarian_nonexistent = get_librarian_for_library(999)
    print(f"   Librarian for non-existent library: {librarian_nonexistent}")


if __name__ == "__main__":
    # Clear existing data
    print("Clearing existing data...")
    Librarian.objects.all().delete()
    Library.objects.all().delete()
    Book.objects.all().delete()
    Author.objects.all().delete()
    
    # Create sample data and test
    data = create_sample_data()
    test_query_functions(data)
    
    print("\n" + "="*50)
    print("ALL TESTS COMPLETED SUCCESSFULLY!")
    print("="*50)
