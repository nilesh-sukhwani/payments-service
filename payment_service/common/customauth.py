import jwt
from rest_framework import authentication, exceptions

from payment_service.common.exceptions import (
    ApplicationNotFound,
    CredentialsNotProvided,
)
from payment_service.users.models import ApplicationMaster


class CustomAuthentication(authentication.BaseAuthentication):
    @staticmethod
    def verify_token(request, app_id, auth):
        """[verify the token provided in Application Token table and retun an application object to \
        overide the default authentication]

        Arguments:
            request {[type]} -- [description]
            auth {[id]} -- [access token]

        Raises:
            ApplicationNotFound: [When Application is not registered with us]
            TokenExpired: [When the token is expired and the Application tried to access the secured API]

        Returns:
            [application] -- [application obj]
        """
        if ApplicationMaster.objects.filter(access_code=app_id).exists():
            application = ApplicationMaster.objects.get(access_code=app_id)

            try:
                app_public_key = application.public_key.encode()
                decoded_token = jwt.decode(auth, app_public_key, algorithms=["RS256"])

                decoded_app_id = decoded_token.get("id")

                if not decoded_app_id == app_id:
                    raise exceptions.AuthenticationFailed()

            except KeyError:
                raise exceptions.ValidationError()

            return application
        else:
            raise ApplicationNotFound()

    def authenticate(self, request):
        """
        [Function to get the token from the header of the API calls made to the system\
        and override the default authentication provided by the Django to customise on out own.]

        Arguments:
            request {[type]} -- [description]

        Returns:
            [token] -- [app_obj]
        """
        try:
            auth_header_value = request.META.get("HTTP_AUTHORIZATION", "")

            if auth_header_value:
                authmeth, auth = request.META["HTTP_AUTHORIZATION"].split(" ", 1)

                if not authmeth == "bearer" or not auth:
                    raise exceptions.AuthenticationFailed()

            else:
                raise CredentialsNotProvided()

        except KeyError:
            raise ApplicationNotFound()

        if request.data.get("app_id"):
            try:

                app_id = request.data.get("app_id")

                application = self.verify_token(request, app_id, auth)

                return (application, None)

            except KeyError:

                raise exceptions.ValidationError()
        else:
            raise exceptions.ValidationError()
