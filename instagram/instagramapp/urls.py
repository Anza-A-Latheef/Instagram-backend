# instagramapp/urls.py

from django.urls import path
from .views import UserRegistrationView, UserLoginView,PostsViews,CommentViewSet
# urls.py
from rest_framework_simplejwt.views import TokenRefreshView

comment_list = CommentViewSet.as_view({'get': 'list_comments'})
comment_create = CommentViewSet.as_view({'post': 'create'})

 # other paths...
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('post/', PostsViews.as_view(), name='postviews'),
    path('comments/<int:post_id>/', comment_list, name='list-comments'),
    path('comments/', comment_create, name='create-comment'),
    
]
