from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView


# google view
class GoogleLoginView(SocialLoginView):
    metadata_class = GoogleOAuth2Adapter
