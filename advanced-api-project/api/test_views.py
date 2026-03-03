from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from datetime import datetime
from .models import Author, Book


class BookModelTest(TestCase):
    """Test cases for the Book model"""
    
    def setUp(self):
        self.author = Author.objects.create(name="Test Author")
    
    def test_book_creation(self):
        """Test creating a book instance"""
        book = Book.objects.create(
            title="Test Book",
            publication_year=2023,
            author=self.author
        )
        self.assertEqual(book.title, "Test Book")
        self.assertEqual(book.publication_year, 2023)
        self.assertEqual(book.author, self.author)
        self.assertEqual(str(book), "Test Book (2023)")
    
    def test_book_ordering(self):
        """Test default ordering of books"""
        book1 = Book.objects.create(
            title="Old Book",
            publication_year=2020,
            author=self.author
        )
        book2 = Book.objects.create(
            title="New Book",
            publication_year=2023,
            author=self.author
        )
        books = Book.objects.all()
        self.assertEqual(books[0], book2)  # Newer book first
        self.assertEqual(books[1], book1)  # Older book second


class AuthorModelTest(TestCase):
    """Test cases for the Author model"""
    
    def test_author_creation(self):
        """Test creating an author instance"""
        author = Author.objects.create(name="Test Author")
        self.assertEqual(author.name, "Test Author")
        self.assertEqual(str(author), "Test Author")
    
    def test_author_book_relationship(self):
        """Test the one-to-many relationship between Author and Book"""
        author = Author.objects.create(name="Test Author")
        book1 = Book.objects.create(
            title="Book 1",
            publication_year=2021,
            author=author
        )
        book2 = Book.objects.create(
            title="Book 2",
            publication_year=2022,
            author=author
        )
        
        self.assertEqual(author.books.count(), 2)
        self.assertIn(book1, author.books.all())
        self.assertIn(book2, author.books.all())


class BookAPITest(APITestCase):
    """Test cases for Book API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2023,
            author=self.author
        )
    
    def test_get_book_list(self):
        """Test retrieving the list of books"""
        url = reverse('book-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_get_book_detail(self):
        """Test retrieving a single book"""
        url = reverse('book-detail', kwargs={'pk': self.book.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')
    
    def test_create_book_unauthenticated(self):
        """Test creating a book without authentication (should fail)"""
        url = reverse('book-list-create')
        data = {
            'title': 'New Book',
            'publication_year': 2024,
            'author': self.author.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_book_authenticated(self):
        """Test creating a book with authentication"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('book-list-create')
        data = {
            'title': 'New Book',
            'publication_year': 2024,
            'author': self.author.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
    
    def test_create_book_future_year(self):
        """Test creating a book with future publication year (should fail)"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('book-list-create')
        future_year = datetime.now().year + 1
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_book(self):
        """Test updating a book"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('book-detail', kwargs={'pk': self.book.pk})
        data = {
            'title': 'Updated Book',
            'publication_year': 2023,
            'author': self.author.pk
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')
    
    def test_delete_book(self):
        """Test deleting a book"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('book-detail', kwargs={'pk': self.book.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)


class AuthorAPITest(APITestCase):
    """Test cases for Author API endpoints"""
    
    def setUp(self):
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2023,
            author=self.author
        )
    
    def test_get_author_list(self):
        """Test retrieving the list of authors"""
        url = reverse('author-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_get_author_detail(self):
        """Test retrieving a single author with nested books"""
        url = reverse('author-detail', kwargs={'pk': self.author.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Author')
        self.assertEqual(len(response.data['books']), 1)
        self.assertEqual(response.data['books_count'], 1)


class BookFilteringTest(APITestCase):
    """Test cases for Book filtering, searching, and ordering"""
    
    def setUp(self):
        self.author1 = Author.objects.create(name="Author One")
        self.author2 = Author.objects.create(name="Author Two")
        
        self.book1 = Book.objects.create(
            title="Python Programming",
            publication_year=2021,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title="Django Development",
            publication_year=2022,
            author=self.author1
        )
        self.book3 = Book.objects.create(
            title="JavaScript Guide",
            publication_year=2023,
            author=self.author2
        )
    
    def test_filter_by_author(self):
        """Test filtering books by author"""
        url = reverse('book-list-create')
        response = self.client.get(url, {'author': self.author1.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_filter_by_publication_year(self):
        """Test filtering books by publication year"""
        url = reverse('book-list-create')
        response = self.client.get(url, {'publication_year': 2022})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Django Development')
    
    def test_search_by_title(self):
        """Test searching books by title"""
        url = reverse('book-list-create')
        response = self.client.get(url, {'search': 'Python'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Python Programming')
    
    def test_search_by_author_name(self):
        """Test searching books by author name"""
        url = reverse('book-list-create')
        response = self.client.get(url, {'search': 'Two'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'JavaScript Guide')
    
    def test_ordering_by_title(self):
        """Test ordering books by title"""
        url = reverse('book-list-create')
        response = self.client.get(url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data['results']]
        self.assertEqual(titles, ['Django Development', 'JavaScript Guide', 'Python Programming'])
    
    def test_ordering_by_publication_year(self):
        """Test ordering books by publication year"""
        url = reverse('book-list-create')
        response = self.client.get(url, {'ordering': 'publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, [2021, 2022, 2023])


class AuthorFilteringTest(APITestCase):
    """Test cases for Author searching and ordering"""
    
    def setUp(self):
        self.author1 = Author.objects.create(name="Alice Smith")
        self.author2 = Author.objects.create(name="Bob Johnson")
        self.author3 = Author.objects.create(name="Charlie Brown")
    
    def test_search_authors(self):
        """Test searching authors by name"""
        url = reverse('author-list')
        response = self.client.get(url, {'search': 'Bob'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Bob Johnson')
    
    def test_order_authors_by_name(self):
        """Test ordering authors by name"""
        url = reverse('author-list')
        response = self.client.get(url, {'ordering': 'name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [author['name'] for author in response.data['results']]
        self.assertEqual(names, ['Alice Smith', 'Bob Johnson', 'Charlie Brown'])
