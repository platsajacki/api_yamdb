from django.urls import path, include
from rest_framework import routers

from .views import (
    UserRegistrationView, UserTokenView,
    # UserViewSet
    TitleViewSet, CategoryViewSet, GenreViewSet
)

router = routers.DefaultRouter()
# router.register(r'users', UserViewSet, basename='users')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')

urlpatterns = [
    # path('v1/', include(router.urls)),
    path(
        'v1/auth/signup/',
        UserRegistrationView.as_view(),
        name='registration'
    ),
    path(
        'v1/auth/token/',
        UserTokenView.as_view(),
        name='token'
    ),
]
