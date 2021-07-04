import requests
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from rest_auth.registration.serializers import SocialLoginSerializer
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

class GoogleTokenIdAdapter(GoogleOAuth2Adapter):
    token_info_url = "https://oauth2.googleapis.com/tokeninfo"
    def complete_login(self, request, app, token, **kwargs):
        resp = requests.get(
            self.token_info_url,
            params={"id_token": token}
        )
        resp.raise_for_status()
        extra_data = resp.json()
        login = self.get_provider().sociallogin_from_response(request, extra_data)
        return login

# google view
class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleTokenIdAdapter
    client_class = OAuth2Client
    serializer_class = SocialLoginSerializer
    callback_url = 'https://sembada.ihfazh.com/accounts/google/login/callback/'


    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)
