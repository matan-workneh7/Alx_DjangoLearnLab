# Social Media API

A comprehensive Django REST Framework API for a social media platform with user authentication, posts, comments, follows, and notifications.

## Features

### ✅ Task 0: Project Setup and User Authentication
- **Custom User Model**: Extended Django User with bio, profile picture, and follow relationships
- **Token Authentication**: Secure token-based authentication using Django REST Framework
- **User Registration**: Complete registration with email validation and password requirements
- **User Login/Logout**: Secure authentication with token management
- **Profile Management**: Update user profile information and extended profile data

### ✅ Task 1: Posts and Comments Functionality
- **Post Model**: Complete post management with title, content, author, timestamps
- **Comment Model**: Nested comments with parent-child relationships
- **Like Model**: Like/unlike functionality with user tracking
- **CRUD Operations**: Full Create, Read, Update, Delete for posts and comments
- **ViewSets**: Django REST Framework ViewSets with proper permissions
- **Filtering**: Search by title/content, filter by author, date, visibility
- **Pagination**: Automatic pagination with configurable page size
- **Permissions**: Author-only editing, soft delete for comments

### 🚀 Upcoming Features
- **User Follows**: Follow/unfollow users and view follower/following lists
- **Feed System**: Personalized feed showing posts from followed users
- **Notifications**: Real-time notifications for likes, comments, and follows

## API Endpoints

### Authentication Endpoints

#### User Registration
```
POST /api/auth/register/
Content-Type: application/json

{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "first_name": "John",
    "last_name": "Doe"
}
```

**Response:**
```json
{
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "bio": "",
        "profile_picture": null,
        "date_joined": "2024-01-01T12:00:00Z",
        "followers_count": 0,
        "following_count": 0,
        "is_following": false
    },
    "token": "abc123def456ghi789"
}
```

#### User Login
```
POST /api/auth/login/
Content-Type: application/json

{
    "username": "johndoe",
    "password": "securepassword123"
}
```

**Response:**
```json
{
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "bio": "",
        "profile_picture": null,
        "date_joined": "2024-01-01T12:00:00Z",
        "followers_count": 0,
        "following_count": 0,
        "is_following": false
    },
    "token": "abc123def456ghi789"
}
```

#### User Logout
```
POST /api/auth/logout/
Authorization: Token abc123def456ghi789
```

**Response:**
```json
{
    "message": "Successfully logged out."
}
```

### User Profile Endpoints

#### Get Current User Profile
```
GET /api/auth/me/
Authorization: Token abc123def456ghi789
```

#### Update User Profile
```
PUT /api/auth/profile/
Authorization: Token abc123def456ghi789
Content-Type: application/json

{
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "bio": "Software developer and tech enthusiast",
    "profile_picture": "image_file"
}
```

#### Get User Details
```
GET /api/auth/users/1/
Authorization: Token abc123def456ghi789
```

#### List Users
```
GET /api/auth/users/?search=john
Authorization: Token abc123def456ghi789
```

### Follow/Unfollow Endpoints

#### Follow User
```
POST /api/auth/follow/
Authorization: Token abc123def456ghi789
Content-Type: application/json

{
    "user_id": 2
}
```

#### Unfollow User
```
POST /api/auth/unfollow/
Authorization: Token abc123def456ghi789
Content-Type: application/json

{
    "user_id": 2
}
```

#### Get Following List
```
GET /api/auth/following/
Authorization: Token abc123def456ghi789
```

#### Get Followers List
```
GET /api/auth/followers/
Authorization: Token abc123def456ghi789
```

### Posts Endpoints

#### List Posts
```
GET /api/posts/
Authorization: Token abc123def456ghi789
Query Parameters:
- page: Page number (default: 1)
- search: Search in title/content
- author: Filter by author ID
- is_public: Filter by visibility
- ordering: Sort order (created_at, -created_at)
```

#### Create Post
```
POST /api/posts/
Authorization: Token abc123def456ghi789
Content-Type: application/json

{
    "title": "My First Post",
    "content": "This is the content of my first post...",
    "is_public": true
}
```

#### Get Post Details
```
GET /api/posts/{id}/
Authorization: Token abc123def456ghi789
```

#### Update Post
```
PUT /api/posts/{id}/
Authorization: Token abc123def456ghi789
Content-Type: application/json

{
    "title": "Updated Post Title",
    "content": "Updated content...",
    "is_public": false
}
```

#### Delete Post
```
DELETE /api/posts/{id}/
Authorization: Token abc123def456ghi789
```

#### Like/Unlike Post
```
POST /api/posts/{id}/like/
Authorization: Token abc123def456ghi789
```

#### Get Post Likes
```
GET /api/posts/{id}/likes/
Authorization: Token abc123def456ghi789
```

### Comments Endpoints

#### List Comments
```
GET /api/comments/
Authorization: Token abc123def456ghi789
Query Parameters:
- page: Page number
- post: Filter by post ID
- author: Filter by author ID
- ordering: Sort order
```

#### Create Comment
```
POST /api/comments/
Authorization: Token abc123def456ghi789
Content-Type: application/json

{
    "content": "Great post!",
    "post": 1,
    "parent": null
}
```

#### Update Comment
```
PUT /api/comments/{id}/
Authorization: Token abc123def456ghi789
Content-Type: application/json

{
    "content": "Updated comment content..."
}
```

#### Delete Comment
```
DELETE /api/comments/{id}/
Authorization: Token abc123def456ghi789
```

#### Get Comment Replies
```
GET /api/comments/{id}/replies/
Authorization: Token abc123def456ghi789
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Django 6.0+
- Django REST Framework
- django-filter (for filtering)
- Pillow (for image uploads)

### Installation

1. **Clone repository:**
   ```bash
   git clone <repository-url>
   cd social_media_api
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install djangorestframework django-filter django-cors-headers Pillow
   ```

4. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server:**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`

## Authentication

### Token Authentication
The API uses Token Authentication. Include the token in the Authorization header:

```
Authorization: Token your_token_here
```

### Getting a Token
You get a token when you register or login. Use the `/api/auth/login/` endpoint to get a new token.

### Refresh Token
Use `/api/auth/token-refresh/` to get a new token with your credentials.

## User Model

### Custom User Fields
- **username**: Unique username (required)
- **email**: User email (required, unique)
- **first_name**: User's first name
- **last_name**: User's last name
- **bio**: User biography (max 500 characters)
- **profile_picture**: Profile image file
- **followers**: Users following this user (ManyToMany)
- **following**: Users this user follows (ManyToMany)
- **date_joined**: When the user was created
- **updated_at**: When the user was last updated

### Extended Profile
Additional profile information stored in UserProfile model:
- **website**: Personal website URL
- **location**: User's location
- **birth_date**: Date of birth
- **is_verified**: Verified account status

## Error Handling

### Standard Error Responses
```json
{
    "error": "Error message description"
}
```

### Validation Errors
```json
{
    "field_name": ["Error message for this field"],
    "another_field": ["Error message for another field"]
}
```

### HTTP Status Codes
- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Testing

### Using curl

**Register a user:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

**Login:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

**Get user profile:**
```bash
curl -X GET http://127.0.0.1:8000/api/auth/me/ \
  -H "Authorization: Token your_token_here"
```

### Using Postman
1. Import the provided Postman collection (if available)
2. Set the base URL to `http://127.0.0.1:8000`
3. Use the authentication endpoints to get a token
4. Add the token to the Authorization header for authenticated requests

## Security Features

- **Token Authentication**: Secure token-based authentication
- **Password Validation**: Django's built-in password validators
- **CORS Protection**: Configured for frontend integration
- **Input Validation**: Comprehensive form validation
- **Permission Classes**: Proper authorization checks
- **CSRF Protection**: Enabled for session authentication

## Development

### Project Structure
```
social_media_api/
├── social_media_api/          # Main project directory
│   ├── settings.py           # Project settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── accounts/                 # User authentication app
│   ├── models.py            # Custom user models
│   ├── serializers.py      # User serializers
│   ├── views.py             # User views
│   └── urls.py              # User URL patterns
├── posts/                    # Posts and comments app
│   ├── models.py            # Post, Comment, Like models
│   ├── serializers.py      # Post and comment serializers
│   ├── views.py             # Post and comment ViewSets
│   └── urls.py              # Posts URL patterns
├── media/                    # User uploaded files
├── db.sqlite3               # SQLite database
└── manage.py                # Django management script
```

### Customization
- Modify `posts/models.py` to add custom post fields
- Update `posts/serializers.py` for custom serialization
- Add new ViewSets in `posts/views.py` for additional functionality
- Configure additional filters in ViewSets
- Add custom permissions in `posts/views.py`

## Pagination and Filtering

### Pagination
- **Page Size**: Configurable (default: 20)
- **Page Numbers**: Automatic pagination
- **Metadata**: Total count, next/previous page URLs

### Filtering Options
- **Search**: Search in title and content fields
- **Author Filter**: Filter posts by author
- **Date Filter**: Filter by creation date
- **Visibility Filter**: Filter by public/private status
- **Ordering**: Sort by date, likes, comments count

## API Documentation

### Browsable API
Django REST Framework provides a browsable API at all endpoints. Visit `http://127.0.0.1:8000/api/` in your browser to explore the API.

### Schema Documentation
The API follows REST conventions and uses standard HTTP methods:
- `GET`: Retrieve resources
- `POST`: Create resources
- `PUT/PATCH`: Update resources
- `DELETE`: Remove resources

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For questions and support:
- Check the documentation
- Review the API endpoints
- Create an issue in the repository
- Contact the development team

---

**Note**: This includes the first two phases of the Social Media API project. Additional features like user follows, notifications, and feed functionality will be implemented in subsequent phases.
