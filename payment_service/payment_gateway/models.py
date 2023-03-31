from django.core.validators import RegexValidator
from django.db import models
from django_prometheus.models import ExportModelOperationsMixin

from payment_service.common.models import TimeStampedModel
from payment_service.payment_gateway.constants import (
    ORDER_STATUS_CHOICES,
    PAYMENT_MODE_CHOICES,
)
from payment_service.users.models import ApplicationMaster


class ServiceProvider(ExportModelOperationsMixin("ServiceProvider"), TimeStampedModel):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    business_name = models.CharField(max_length=255)
    contact_person_name = models.CharField(max_length=255)
    contact_person_email = models.EmailField(max_length=254)

    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    contact_person_phone = models.CharField(
        validators=[phone_regex], max_length=17, blank=True
    )  # Validators should be a list

    # working_key = models.CharField(max_length=255)
    # access_code = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Service Providers"


class Transaction(ExportModelOperationsMixin("Transaction"), TimeStampedModel):
    order_id = models.CharField(unique=True, max_length=255)
    amount = models.FloatField()
    tracking_id = models.PositiveBigIntegerField(default=0)
    bank_ref_no = models.PositiveBigIntegerField(default=0)
    request_payload = models.JSONField(default=dict)
    response_payload = models.JSONField(default=dict)
    order_status = models.PositiveIntegerField(default=0, choices=ORDER_STATUS_CHOICES)
    payment_mode = models.PositiveIntegerField(default=0, choices=PAYMENT_MODE_CHOICES)

    currency = models.CharField(
        # choices=Currency.choices,
        max_length=3,
        default="INR",
    )
    transaction_date = models.DateTimeField(null=True, blank=True)

    application_fk = models.ForeignKey(
        ApplicationMaster,
        null=True,
        blank=True,
        related_name="transaction_application",
        on_delete=models.CASCADE,
        db_column="application_fk",
    )
    service_provider_fk = models.ForeignKey(
        ServiceProvider,
        null=True,
        blank=True,
        related_name="transaction_service_provider",
        on_delete=models.CASCADE,
        db_column="service_provider_fk",
    )

    class Meta:
        ordering = ["-created_at"]
