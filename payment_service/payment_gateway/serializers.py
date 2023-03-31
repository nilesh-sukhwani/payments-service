from rest_framework import serializers

from .models import ServiceProvider
from .utils import generate_obj_id


class TransactionSerializer(serializers.Serializer):
    service_provider_id = serializers.PrimaryKeyRelatedField(
        required=False, queryset=ServiceProvider.objects.all()
    )
    order_id = serializers.CharField(required=False)
    currency = serializers.CharField(required=True)
    amount = serializers.FloatField(required=True)
    redirect_url = serializers.CharField(required=False)
    cancel_url = serializers.CharField(required=False)
    language = serializers.CharField(required=False)
    billing_name = serializers.CharField(required=False)
    billing_address = serializers.CharField(required=False)
    billing_city = serializers.CharField(required=False)
    billing_state = serializers.CharField(required=False)
    billing_zip = serializers.CharField(required=False)
    billing_country = serializers.CharField(required=False)
    billing_tel = serializers.CharField(required=False)
    billing_email = serializers.CharField(required=False)
    delivery_name = serializers.CharField(required=False)
    delivery_address = serializers.CharField(required=False)
    delivery_city = serializers.CharField(required=False)
    delivery_state = serializers.CharField(required=False)
    delivery_zip = serializers.CharField(required=False)
    delivery_country = serializers.CharField(required=False)
    delivery_tel = serializers.CharField(required=False)
    merchant_param1 = serializers.CharField(required=False)
    merchant_param2 = serializers.CharField(required=False)
    merchant_param3 = serializers.CharField(required=False)
    merchant_param4 = serializers.CharField(required=False)
    merchant_param5 = serializers.CharField(required=False)
    promo_code = serializers.CharField(required=False)
    customer_identifier = serializers.CharField(required=False)

    def validate(self, data):
        order_id = data.get("order_id")

        if not order_id:
            order_id = generate_obj_id()
            data["order_id"] = order_id
        return data


class CCAvenuePaymentRequestSerializer(serializers.Serializer):
    app_request = serializers.CharField(required=True)
    app_id = serializers.CharField(required=True)


class CCAvenuePaymentResponseSerializer(serializers.Serializer):
    encResp = serializers.CharField(required=True)
    orderNo = serializers.CharField(required=True)
    # crossSellUrl = serializers.CharField(required=False)


class CCAvenueStatusSerializer(serializers.Serializer):
    reference_no = serializers.CharField(required=False, max_length=255)
    order_no = serializers.CharField(required=False, max_length=255)

    def validate(self, data):
        """
        Validation of reference_no and order_no.
        """
        reference_no = data.get("reference_no")
        order_no = data.get("order_no")

        if not reference_no and not order_no:
            raise serializers.ValidationError(
                "at least one of reference_no or order_no input required."
            )

        return data
