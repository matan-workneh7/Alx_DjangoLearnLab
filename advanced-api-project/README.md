# Advanced API Development with Django REST Framework

This project demonstrates advanced API development concepts using Django REST Framework, including custom serializers, generic views, filtering, searching, ordering, and comprehensive testing.

## Features Implemented

### 1. Custom Serializers with Validation
- **BookSerializer**: Handles Book model serialization with custom validation for publication_year
- **AuthorSerializer**: Includes nested BookSerializer for one-to-many relationship handling
- Custom validation ensures publication_year cannot be in the future
- Enhanced AuthorSerializer with books_count field

### 2. Generic Views and Custom Views
- **BookListCreateView**: Handles GET (list) and POST (create) operations
- **BookDetailView**: Handles GET (retrieve), PUT/PATCH (update), and DELETE operations
- **AuthorListView**: Handles GET operations for authors with nested books
- **AuthorDetailView**: Handles GET operations for individual authors
- Permission-based access control (authenticated users can modify, read-only for others)

### 3. Filtering, Searching, and Ordering
- **Filtering**: Filter books by title, author, and publication_year
- **Searching**: Search books by title and author name
- **Ordering**: Order results by title, publication_year, or author name
- Applied to both Book and Author endpoints

### 4. Comprehensive Unit Testing
- **Model Tests**: Test Author and Book model functionality
- **API Tests**: Test all CRUD operations for both models
- **Permission Tests**: Verify authentication requirements
- **Validation Tests**: Test custom validation logic
- **Filtering Tests**: Test filtering, searching, and ordering functionality
- 21 comprehensive test cases with 100% pass rate

## API Endpoints

### Books
- `GET /api/books/` - List all books (with filtering, searching, ordering)
- `POST /api/books/` - Create a new book (requires authentication)
- `GET /api/books/<id>/` - Retrieve a specific book
- `PUT/PATCH /api/books/<id>/` - Update a book (requires authentication)
- `DELETE /api/books/<id>/` - Delete a book (requires authentication)

### Authors
- `GET /api/authors/` - List all authors (with searching and ordering)
- `GET /api/authors/<id>/` - Retrieve a specific author with nested books

## Query Parameters

### Filtering Books
- `?author=<author_id>` - Filter by author
- `?publication_year=<year>` - Filter by publication year
- `?title=<title>` - Filter by title

### Searching
- `?search=<query>` - Search in title and author name fields

### Ordering
- `?ordering=title` - Order by title (ascending)
- `?ordering=-title` - Order by title (descending)
- `?ordering=publication_year` - Order by publication year
- `?ordering=author__name` - Order by author name

## Models

### Author
- `name`: CharField (max_length=100)
- Relationship: One-to-many with Book model

### Book
- `title`: CharField (max_length=200)
- `publication_year`: IntegerField
- `author`: ForeignKey to Author model
- Validation: publication_year cannot be in the future

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install django djangorestframework django-filter
   ```

2. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create Superuser** (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

4. **Run Tests**:
   ```bash
   python manage.py test api
   ```

5. **Start Development Server**:
   ```bash
   python manage.py runserver
   ```

## Testing

The project includes comprehensive unit tests covering:
- Model functionality and relationships
- API endpoint operations (CRUD)
- Authentication and permissions
- Custom validation logic
- Filtering, searching, and ordering

Run tests with: `python manage.py test api`

## Usage Examples

### Create a Book (Authenticated)
```bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic your_credentials" \
  -d '{
    "title": "Django for Beginners",
    "publication_year": 2023,
    "author": 1
  }'
```

### List Books with Filtering
```bash
curl "http://localhost:8000/api/books/?author=1&publication_year=2023"
```

### Search Books
```bash
curl "http://localhost:8000/api/books/?search=django"
```

### Order Books
```bash
curl "http://localhost:8000/api/books/?ordering=-publication_year"
```

### Get Author with Books
```bash
curl "http://localhost:8000/api/authors/1/"
```

## Project Structure

```
advanced-api-project/
├── advanced_api_project/
│   ├── __init__.py
│   ├── settings.py          # DRF configuration
│   ├── urls.py             # Main URL routing
│   └── wsgi.py
├── api/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py           # Author and Book models
│   ├── serializers.py      # Custom serializers with validation
│   ├── views.py            # Generic views with filtering/searching
│   ├── urls.py             # API URL routing
│   └── test_views.py       # Comprehensive unit tests
├── manage.py
└── db.sqlite3
```

## Key Concepts Demonstrated

1. **Custom Serializers**: Nested serialization and custom validation
2. **Generic Views**: Efficient CRUD operations using DRF's generic views
3. **Permissions**: Role-based access control
4. **Filtering**: DjangoFilterBackend integration
5. **Searching**: SearchFilter for text-based queries
6. **Ordering**: OrderingFilter for result sorting
7. **Testing**: Comprehensive test coverage using APITestCase
8. **Documentation**: Inline documentation and README

This implementation follows Django REST Framework best practices and demonstrates advanced API development concepts suitable for production use.
