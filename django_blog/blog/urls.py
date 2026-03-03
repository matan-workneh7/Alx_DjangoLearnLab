from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    
    # Home and Blog URLs
    path('', views.home_view, name='home'),
    path('search/', views.search_view, name='search'),
    path('tags/<slug:slug>/', views.posts_by_tag_view, name='posts_by_tag'),
    
    # Post URLs
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    # Comment URLs
    path('post/<int:post_id>/comments/new/', views.comment_create_view, name='comment_create'),
    path('comment/<int:comment_id>/update/', views.comment_edit_view, name='comment_edit'),
    path('comment/<int:comment_id>/delete/', views.comment_delete_view, name='comment_delete'),
]
