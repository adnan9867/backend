from django.urls import path
from .views import *

urlpatterns = [

    # User Profile Endpoints
    path('sign_up', UserSignupView.as_view({'post': 'create'}), name='sign_up'),
    path('login', UserLoginViewSet.as_view({'post': 'create'}), name='sign_up'),
    path('user_profile', UserProfileViewSet.as_view({'get': 'list'}), name='sign_up'),
    path('user_profile_list', UserProfileListViewSet.as_view({'get': 'list'}), name='sign_up'),

    # Post Endpoints
    path('post', PostViewSet.as_view({'get': 'list', 'post': 'create'}), name='post'),
    path('update_post', PostViewSet.as_view({'put': 'update'}), name='update_post'),
    path('delete_post', PostViewSet.as_view({'delete': 'destroy'}), name='delete_post'),
    path('post_listing', PostListViewSet.as_view({'get': 'list'}), name='post_listing'),

    # Post Reaction Endpoints
    path('post_like_unlike', PostReactionViewSet.as_view({'post': 'post_like'}), name='post_like'),

]
