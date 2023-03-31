from django.apps import AppConfig


class PaymentGatewayConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "payment_service.payment_gateway"
    verbose_name = "Payment Gateway"
    label = "payment_gateway"
