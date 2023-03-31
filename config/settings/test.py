"""
With these settings, tests run faster.
"""

from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="pc11xQ0x6Se0uTKYDnMGMMQOY6GwpRLtA2hB69SrS5cjlx8DEIxlkG66fmLNOWW6",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
# EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# DEBUGING FOR TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES[0]["OPTIONS"]["debug"] = True  # type: ignore # noqa F405

# Your stuff...
# ------------------------------------------------------------------------------

# == CC AVENUE Secret Variables ==
CCAVENUE_MERCHANT_CODE = env.str("CCAVENUE_MERCHANT_CODE", "")
CCAVENUE_WORKING_KEY = env.str("CCAVENUE_WORKING_KEY", "")
CCAVENUE_ACCESS_CODE = env.str("CCAVENUE_ACCESS_CODE", "")
CCAVENUE_REDIRECT_URL: str = env.str("CCAVENUE_REDIRECT_URL", "")
CCAVENUE_CANCEL_URL: str = env.str("CCAVENUE_CANCEL_URL", "")
CCAVENUE_PAYMENT_URL: str = env.str("CCAVENUE_PAYMENT_URL", "")
CCAVENUE_STATUS_API_URL: str = env.str("CCAVENUE_STATUS_API_URL", "")

# == EMAIL ==
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL")
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_TIMEOUT = None
