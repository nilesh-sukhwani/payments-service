from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_prometheus.models import ExportModelOperationsMixin

from payment_service.common.models import TimeStampedModel


class User(ExportModelOperationsMixin("User"), AbstractUser):
    """
    Default custom user model for payment_service.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class ApplicationMaster(ExportModelOperationsMixin("ApplicationMaster"), TimeStampedModel):
    name = models.CharField(max_length=255)
    application_config = models.JSONField(default=dict)

    working_key = models.CharField(unique=True, max_length=255)
    access_code = models.CharField(unique=True, max_length=255)

    public_key = models.TextField()

    redirect_url = models.URLField(max_length=200)
    cancel_url = models.URLField(max_length=200)

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Applications"
        ordering = ["-created_at"]
