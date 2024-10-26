# instagramapp/urls.py

from django.urls import path
from .views import UserRegistrationView, UserLoginView,PostsViews
# urls.py
from rest_framework_simplejwt.views import TokenRefreshView

 # other paths...
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('post/', PostsViews.as_view(), name='postviews'),
    
]
