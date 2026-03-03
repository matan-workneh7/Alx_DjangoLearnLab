from django.urls import path
from . import views

urlpatterns = [
    # Home and Blog URLs
    path('', views.home_view, name='home'),
    path('search/', views.search_view, name='search'),
    path('tags/<slug:slug>/', views.posts_by_tag_view, name='posts_by_tag'),
    
    # Post URLs
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/new/', views.PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    # Comment URLs
    path('posts/<int:post_id>/comment/', views.comment_create_view, name='comment_create'),
    path('comments/<int:comment_id>/edit/', views.comment_edit_view, name='comment_edit'),
    path('comments/<int:comment_id>/delete/', views.comment_delete_view, name='comment_delete'),
]
