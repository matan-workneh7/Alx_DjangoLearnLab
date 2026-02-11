# Django Advanced Features and Security Project

This project demonstrates the implementation of advanced Django features focusing on custom user models, permissions, security best practices, and secure communication.

## Project Structure

```
LibraryProject/
├── LibraryProject/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py          # Security configurations and custom user model
│   ├── urls.py
│   └── wsgi.py
├── relationship_app/
│   ├── management/
│   │   └── commands/
│   │       └── setup_groups.py  # Command to create groups and permissions
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py             # Custom user model admin configuration
│   ├── apps.py
│   ├── forms.py             # Secure form handling
│   ├── models.py            # Custom user model and permissions
│   ├── templates/
│   │   └── relationship_app/
│   │       ├── add_book.html
│   │       ├── edit_book.html
│   │       ├── delete_book.html
│   │       ├── list_books.html
│   │       ├── login.html
│   │       ├── logout.html
│   │       └── register.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py             # Permission-protected views
├── manage.py
└── requirements.txt
```

## Features Implemented

### 1. Custom User Model

**Location:** `relationship_app/models.py`

- **CustomUser**: Extends `AbstractUser` with additional fields:
  - `date_of_birth`: Date field for user's birth date
  - `profile_photo`: Image field for user profile picture
- **CustomUserManager**: Custom manager with:
  - `create_user()`: Handles user creation with custom fields
  - `create_superuser()`: Creates admin users with required permissions

**Configuration:** `settings.py`
```python
AUTH_USER_MODEL = 'relationship_app.CustomUser'
```

### 2. Permissions and Groups System

**Custom Permissions:** Added to Book model
- `can_view`: Permission to view books
- `can_create`: Permission to create books
- `can_edit`: Permission to edit books
- `can_delete`: Permission to delete books

**Groups Setup:**
- **Admins**: All permissions
- **Editors**: `can_create` and `can_edit` permissions
- **Viewers**: `can_view` permission only

**Setup Command:**
```bash
python manage.py setup_groups
```

### 3. Security Configurations

**Security Settings in `settings.py`:**
- `SECURE_BROWSER_XSS_FILTER`: Enables XSS filter in browsers
- `X_FRAME_OPTIONS`: Set to 'DENY' to prevent clickjacking
- `SECURE_CONTENT_TYPE_NOSNIFF`: Prevents MIME-type sniffing
- `CSRF_COOKIE_SECURE`: Ensures CSRF cookies are sent over HTTPS only
- `SESSION_COOKIE_SECURE`: Ensures session cookies are sent over HTTPS only
- `SECURE_HSTS_*`: HSTS settings for HTTPS enforcement

**Content Security Policy (CSP):**
- `CSP_DEFAULT_SRC`: Restricts content sources to self only
- `CSP_SCRIPT_SRC`: Allows scripts from self only
- `CSP_STYLE_SRC`: Allows styles from self and inline styles
- `CSP_IMG_SRC`: Allows images from self and data URIs
- `CSP_FONT_SRC`: Allows fonts from self only

### 4. Secure Views and Templates

**View Security:**
- All views use `@login_required` decorator
- Permission-based access control using `@permission_required`
- Secure form handling with Django forms
- SQL injection prevention using Django ORM
- XSS prevention with template escaping

**Template Security:**
- All forms include `{% csrf_token %}`
- Output escaped using `|escape` filter
- Secure search functionality with parameterized queries

### 5. Admin Integration

**Custom User Admin:**
- Extended `UserAdmin` for `CustomUser`
- Custom fieldsets for additional fields
- Proper display and filtering options

## Installation and Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create Superuser:**
   ```bash
   python manage.py createsuperuser
   ```

4. **Setup Groups and Permissions:**
   ```bash
   python manage.py setup_groups
   ```

5. **Run Development Server:**
   ```bash
   python manage.py runserver
   ```

## Security Measures Documentation

### Authentication and Authorization
- Custom user model with additional fields
- Role-based access control through UserProfile
- Permission decorators on sensitive views
- Group-based permission management

### Data Protection
- CSRF protection on all forms
- XSS prevention through template escaping
- SQL injection prevention using Django ORM
- Secure password validation

### Secure Communication
- HTTPS-only cookies configuration
- HSTS headers for HTTPS enforcement
- Content Security Policy implementation
- Clickjacking protection

### Input Validation
- Django forms for input validation
- Parameterized database queries
- Output encoding in templates
- Secure search functionality

## Testing the Implementation

1. **Create Test Users:**
   - Create users with different roles (Admin, Librarian, Member)
   - Assign users to appropriate groups

2. **Test Permissions:**
   - Log in as different user types
   - Verify access restrictions on book operations
   - Test permission enforcement

3. **Security Testing:**
   - Verify CSRF tokens are present
   - Test XSS prevention
   - Check secure cookie settings
   - Verify CSP headers

## Usage Examples

### Creating a User with Custom Fields
```python
from relationship_app.models import CustomUser

user = CustomUser.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='securepassword',
    date_of_birth='1990-01-01'
)
```

### Checking Permissions in Views
```python
from django.contrib.auth.decorators import permission_required

@permission_required('relationship_app.can_edit', raise_exception=True)
def edit_book(request, book_id):
    # View logic here
    pass
```

### Template Permission Checks
```html
{% if perms.relationship_app.can_create %}
    <a href="{% url 'add_book' %}">Add Book</a>
{% endif %}
```

## Security Best Practices Implemented

1. **Never trust user input** - All input is validated and sanitized
2. **Principle of least privilege** - Users only have necessary permissions
3. **Defense in depth** - Multiple layers of security controls
4. **Secure by default** - Security settings enabled by default
5. **Regular updates** - Using latest Django version with security patches

This project serves as a comprehensive example of implementing security best practices in Django applications while maintaining functionality and user experience.
