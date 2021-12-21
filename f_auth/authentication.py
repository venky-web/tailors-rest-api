from rest_framework import authentication
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials

from .exceptions import FirebaseError, InvalidAuthToken, NoAuthToken
import env_variables

cred = credentials.Certificate(env_variables.FIREBASE_CONFIG_FILE)
firebase_app = firebase_admin.initialize_app(cred)


def return_email(self):
    return self.email


class FirebaseAuthentication(authentication.BaseAuthentication):
    """Default authentication for the app"""

    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            raise NoAuthToken("No auth token provided")

        id_token = auth_header.split(" ").pop()
        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception:
            raise InvalidAuthToken("Invalid auth token")

        if not id_token or not decoded_token:
            return None

        try:
            uid = decoded_token.get("uid")
        except Exception:
            raise FirebaseError()

        auth_user = auth.get_user(uid)
        auth_user.is_authenticated = property(True)
        setattr(auth_user, "__str__", return_email)
        return auth_user, None

