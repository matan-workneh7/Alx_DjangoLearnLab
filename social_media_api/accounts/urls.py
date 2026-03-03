from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# No ViewSets for now, using GenericAPIView classes

urlpatterns = [
    # Authentication endpoints
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('logout/', views.UserLogoutView.as_view(), name='user-logout'),
    path('token-refresh/', views.token_refresh_view, name='token-refresh'),
    
    # User profile endpoints
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('profile/extended/', views.UpdateExtendedProfileView.as_view(), name='extended-profile'),
    path('users/<int:pk>/', views.UserProfileDetailView.as_view(), name='user-detail'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('me/', views.current_user_view, name='current-user'),
    path('stats/<int:user_id>/', views.user_stats_view, name='user-stats'),
    
    # Follow/Unfollow endpoints
    path('follow/<int:user_id>/', views.follow_user_view, name='follow-user'),
    path('unfollow/<int:user_id>/', views.unfollow_user_view, name='unfollow-user'),
    path('following/', views.UserFollowingListView.as_view(), name='user-following'),
    path('followers/', views.UserFollowersListView.as_view(), name='user-followers'),
]
