import json

import django.shortcuts
import requests
from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseRedirect
from rest_framework import permissions, status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from payment_service.common import api_utils
from payment_service.common.customauth import CustomAuthentication
from payment_service.common.exceptions import ApplicationNotFound
from payment_service.payment_gateway.ccavenue import CCAvenue
from payment_service.payment_gateway.constants import (
    CCAVENUE_SUCCESS_STATUS,
    GET_ORDER_STATUS,
    ORDER_STATUS,
    PAYMENT_MODE_DICT,
    REQUEST_TYPE,
    RESPONSE_TYPE,
    VERSION,
)
from payment_service.payment_gateway.helpers import (
    create_transaction,
    get_response_as_per_response_type,
    get_response_html,
    send_mail_to_user,
)
from payment_service.payment_gateway.models import Transaction
from payment_service.payment_gateway.serializers import (
    CCAvenuePaymentRequestSerializer,
    CCAvenuePaymentResponseSerializer,
    CCAvenueStatusSerializer,
    TransactionSerializer,
)
from payment_service.payment_gateway.utils import (
    decrypt,
    encrypt,
    get_decrypted_response_html,
)
from payment_service.users.models import ApplicationMaster


class CCAvenueRequestView(APIView):
    """
    View to get CCAvenue Payment link.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    authentication_classes = [CustomAuthentication]
    permission_classes = []
    serializer_class = CCAvenuePaymentRequestSerializer

    def post(self, request, **kwargs):
        """
        :param request: Request - drf request object to get incoming data from
        :return: CCAvenue payment api endpoint: dict
        """
        response_type = request.data.get("response_type", None)
        application_working_key = request.user.working_key

        if response_type == "HTML":
            content_type = "text/html"
        else:
            content_type = "application/json"

        validated_payload = api_utils.deserialize_request(
            request=request,
            serializer_class=self.serializer_class,
        )

        payment_paylaod = decrypt(
            validated_payload.get("app_request"), application_working_key
        )

        json_payment_payload = json.loads(payment_paylaod)

        serializer = TransactionSerializer(
            data=json_payment_payload, context={"request": request}
        )

        if serializer.is_valid(raise_exception=True):
            validated_data: object = serializer.validated_data

        create_transaction(request, validated_data)

        ccavenue_api_client = CCAvenue(
            working_key=settings.CCAVENUE_WORKING_KEY,
            access_code=settings.CCAVENUE_ACCESS_CODE,
            merchant_code=settings.CCAVENUE_MERCHANT_CODE,
            redirect_url=settings.CCAVENUE_REDIRECT_URL,
            cancel_url=settings.CCAVENUE_CANCEL_URL,
        )

        encrypted_data = ccavenue_api_client.encrypt(validated_data)

        return Response(
            data=get_response_as_per_response_type(response_type, encrypted_data),
            status=status.HTTP_200_OK,
            content_type=content_type,
        )


class CCAvenueResponseView(APIView):
    """
    View to handle CCAvenue response
    """

    authentication_classes = []
    permission_classes = []
    serializer_class = CCAvenuePaymentResponseSerializer

    def post(self, request, **kwargs):
        """
        1. UPDATE Transaction table
        2. Send data to redirect_url of specific application
        3. SEND MAIL
        """

        validated_payload = api_utils.deserialize_request(
            request=request,
            serializer_class=self.serializer_class,
        )

        decrypted_plain_text = decrypt(
            validated_payload.get("encResp"), settings.CCAVENUE_WORKING_KEY
        )
        decrypted_data = dict(
            item.split("=") for item in decrypted_plain_text.split("&") if item
        )

        order_id = validated_payload.get("orderNo")

        try:
            transaction = Transaction.objects.get(order_id=order_id)
        except Transaction.DoesNotExist:
            raise Http404

        txn_status = decrypted_data.get("order_status", 0)
        txn_payment_mode = decrypted_data.get("payment_mode", 0)

        transaction.response_payload = decrypted_data
        transaction.tracking_id = decrypted_data.get("tracking_id", 0)
        transaction.bank_ref_no = decrypted_data.get("bank_ref_no", 0)
        # transaction.transaction_date = response_data.get('trans_date', 0)
        transaction.order_status = ORDER_STATUS.get(txn_status, 0)
        transaction.payment_mode = PAYMENT_MODE_DICT.get(txn_payment_mode, 0)

        transaction.save()

        application_fk = transaction.application_fk

        if application_fk:

            send_mail_to_user(order_id, decrypted_data)

            application_working_key = application_fk.working_key

            encrypted_response = encrypt(decrypted_plain_text, application_working_key)

            # d_dict = {"response": encrypted_response}
            # requests.post(url=application_fk.redirect_url, data=d_dict, json=None)
            # return HttpResponse(get_decrypted_response_html(decrypted_plain_text))
            """
            Redirect to client application
            """
            URL = application_fk.redirect_url + f"?response={encrypted_response}"
            return HttpResponseRedirect(URL)
        else:
            # TODO: add logger here

            # application_fk does not exist in the transaction
            return HttpResponse(get_decrypted_response_html(decrypted_plain_text))


class CCAvenuePaymentCancelView(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = CCAvenuePaymentResponseSerializer

    def post(self, request, **kwargs):
        """
        1. UPDATE Transaction table
        2. Send data to redirect_url of specific application
        3. SEND MAIL
        """

        validated_payload = api_utils.deserialize_request(
            request=request,
            serializer_class=self.serializer_class,
        )

        decrypted_plain_text = decrypt(
            validated_payload.get("encResp"), settings.CCAVENUE_WORKING_KEY
        )
        decrypted_data = dict(
            item.split("=") for item in decrypted_plain_text.split("&") if item
        )

        order_id = validated_payload.get("orderNo")

        try:
            transaction = Transaction.objects.get(order_id=order_id)
        except Transaction.DoesNotExist:
            raise Http404

        txn_status = decrypted_data.get("order_status", 0)
        txn_payment_mode = decrypted_data.get("payment_mode", 0)

        transaction.response_payload = decrypted_data
        transaction.tracking_id = decrypted_data.get("tracking_id", None)
        # transaction.bank_ref_no = decrypted_data.get("bank_ref_no", None)
        # transaction.transaction_date = response_data.get('trans_date', 0)
        transaction.order_status = ORDER_STATUS.get(txn_status, 0)
        transaction.payment_mode = PAYMENT_MODE_DICT.get(txn_payment_mode, 0)

        transaction.save()

        application_fk = transaction.application_fk

        if application_fk:

            send_mail_to_user(order_id, decrypted_data)

            application_working_key = application_fk.working_key

            encrypted_response = encrypt(decrypted_plain_text, application_working_key)

            # d_dict = {"response": encrypted_response}
            # requests.post(url=application_fk.cancel_url, data=d_dict, json=None)
            # return HttpResponse(get_decrypted_response_html(decrypted_plain_text))
            """
            Redirect to client application
            """
            URL = application_fk.cancel_url + f"?response={encrypted_response}"
            return HttpResponseRedirect(URL)

        else:
            # TODO: add logger here
            # application_fk does not exist in the transaction
            return HttpResponse(get_decrypted_response_html(decrypted_plain_text))


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def order_status_view(request):
    serializer = CCAvenueStatusSerializer(data=request.query_params)

    if serializer.is_valid(raise_exception=True):

        params = (
            "?command="
            + GET_ORDER_STATUS
            + "&request_type="
            + REQUEST_TYPE
            + "&response_type="
            + RESPONSE_TYPE
            + "&version="
            + VERSION
            + "&access_code="
            + settings.CCAVENUE_ACCESS_CODE
        )

        request_payload = serializer.validated_data
        reference_no = request_payload.get("reference_no")
        order_no = request_payload.get("order_no")
        dict1 = {"reference_no": reference_no, "order_no": order_no}

        json_req = json.dumps(dict1)
        encryption = encrypt(json_req, settings.CCAVENUE_WORKING_KEY)
        params += "&enc_request=" + encryption
        headers = {"Content-Type": "application/json; charset=utf-8"}

        BASE_URL = settings.CCAVENUE_STATUS_API_URL

        BASE_URL += params

        api_resp = requests.post(BASE_URL, headers=headers, data={})

        response = api_resp.text.split("&")
        length_of_response = len(response)

        workingKey = settings.CCAVENUE_WORKING_KEY

        response_status = status.HTTP_404_NOT_FOUND

        for i in range(length_of_response):

            info_key = response[i].split("=")[0]
            info_value = response[i].split("=")[1]

            if i == (length_of_response - 1):
                info_value = info_value[:-2]

            if info_key == "enc_response":
                dec_resp: str = decrypt(info_value, workingKey)

                dec_resp: dict = json.loads(dec_resp)

                order_status = dec_resp.get("status")

                if order_status == CCAVENUE_SUCCESS_STATUS:

                    response_status = status.HTTP_200_OK
                else:

                    response_status = status.HTTP_404_NOT_FOUND

        return Response(
            data=dec_resp,
            status=response_status,
        )


# ==========================================================================================
# TESTING VIEW FUNCTION AND CLASSES
# ==========================================================================================
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def get_encrypted_payment_response(request):
    return HttpResponse(request.data)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def get_encrypted_data(request):
    access_code = request.query_params.get("access_code")
    payload = request.data

    app_instance = ApplicationMaster.objects.filter(
        access_code=access_code, is_active=True, is_deleted=False
    ).first()
    if app_instance:
        payload_json = json.dumps(payload)

        encRequest = encrypt(payload_json, app_instance.working_key)

        return Response(
            data={"response": encRequest},
            status=status.HTTP_200_OK,
        )
    else:
        raise ApplicationNotFound()


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def get_decrypted_data(request):
    access_code = request.query_params.get("access_code")
    payload = request.data.get("enc_response")

    app_instance = ApplicationMaster.objects.filter(
        access_code=access_code, is_active=True, is_deleted=False
    ).first()

    decResp = decrypt(payload, app_instance.working_key)

    return Response(
        data={"response": json.loads(decResp)},
        status=status.HTTP_200_OK,
    )


@api_view(["GET", "POST"])
@permission_classes([permissions.AllowAny])
def webprint(request):
    return django.shortcuts.render(request, template_name="payment_request_form.html")


class TestCCAvenuePaymentRequest(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    authentication_classes = []
    permission_classes = []
    serializer_class = TransactionSerializer

    def post(self, request, **kwargs):
        """
        Return a list of all users.
        """

        validated_data = api_utils.deserialize_request(
            request=request,
            serializer_class=self.serializer_class,
        )

        transaction = Transaction()
        application = ApplicationMaster.objects.filter(id=2).first()
        transaction.order_id = validated_data.get("order_id")
        transaction.amount = validated_data.get("amount")
        transaction.request_payload = validated_data
        transaction.currency = validated_data.get("currency")
        transaction.service_provider_fk = validated_data.get("service_provider")
        transaction.application_fk = application

        transaction.save()

        ccavenue_api_client = CCAvenue(
            working_key=settings.CCAVENUE_WORKING_KEY,
            access_code=settings.CCAVENUE_ACCESS_CODE,
            merchant_code=settings.CCAVENUE_MERCHANT_CODE,
            redirect_url=settings.CCAVENUE_REDIRECT_URL,
            cancel_url=settings.CCAVENUE_CANCEL_URL,
        )

        encrypted_data = ccavenue_api_client.encrypt(validated_data)

        return HttpResponse(get_response_html(encrypted_data))
