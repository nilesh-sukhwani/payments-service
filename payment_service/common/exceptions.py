from rest_framework import exceptions


class ApplicationNotFound(exceptions.NotAuthenticated):
    status_code = 403
    default_detail = "Application not found"
    default_code = "forbidden"


class CredentialsNotProvided(exceptions.NotAuthenticated):
    status_code = 401
    default_detail = "Authentication credentials were not provided."
    default_code = "not_authenticated"


class DecryptionFailed(exceptions.ParseError):
    status_code = 400
    default_detail = "Decryption Failed, Please Use valid Encryption method"
    default_code = "parse_error"
