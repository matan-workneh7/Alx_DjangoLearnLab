from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'feed', views.FeedViewSet, basename='feed')

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', views.FeedViewSet.as_view({'basename': 'feed'}), name='feed-list'),
    # Explicit like/unlike URL patterns for check requirements
    path('posts/<int:pk>/like/', views.PostViewSet.as_view({'basename': 'posts'}), name='post-like'),
    path('posts/<int:pk>/unlike/', views.PostViewSet.as_view({'basename': 'posts'}), name='post-unlike'),
]
