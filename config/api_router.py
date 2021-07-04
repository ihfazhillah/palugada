from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from sembada.users.api.views import UserViewSet
from sembada.auth.api.views import GoogleLoginView

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)

# SOCIAL AUTH URL
urlpatterns = [
    path("rest-auth/", include('rest_auth.urls')),  # <-login
    path("rest-auth/registration/", include('rest_auth.registration.urls')),  # <- register
    path("auth/google", GoogleLoginView.as_view(), name='google_login'),  # <- google view
]

app_name = "api"
urlpatterns += router.urls
