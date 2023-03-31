from string import Template

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template

from payment_service.payment_gateway.constants import ORDER_STATUS_EMAIL_MESSAGE
from payment_service.payment_gateway.models import Transaction


def create_transaction(request, data):

    transaction = Transaction()
    transaction.service_provider_fk = data.get("service_provider_id")
    transaction.application_fk = request.user
    transaction.order_id = data.get("order_id")
    transaction.amount = data.get("amount")
    transaction.currency = data.get("currency")

    if data.get("service_provider_id"):
        data["service_provider_id"] = data.get("service_provider_id").id

    transaction.request_payload = data

    transaction.save()

    return transaction


def get_response_html(encrypted_req):
    CCAVENUE_URL = settings.CCAVENUE_PAYMENT_URL

    html = """\
    <html>
    <head>
        <title>Sub-merchant checkout page</title>
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
    </head>
    <body>
    <form id="nonseamless" method="post" name="redirect" action="$postUrl"/>
            <input type="hidden" id="encRequest" name="encRequest" value=$encReq>
            <input type="hidden" name="access_code" id="access_code" value=$xscode>
            <script language='javascript'>document.redirect.submit();</script>
    </form>
    </body>
    </html>
    """
    fin = Template(html).safe_substitute(
        postUrl=CCAVENUE_URL, encReq=encrypted_req, xscode=settings.CCAVENUE_ACCESS_CODE
    )

    return fin


def get_response_as_per_response_type(response_type, encrypted_req):
    CCAVENUE_URL = settings.CCAVENUE_PAYMENT_URL

    if response_type == "HTML":
        html = """\
        <html>
        <head>
            <title>Sub-merchant checkout page</title>
            <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
        </head>
        <body>
        <form id="nonseamless" method="post" name="redirect" action="$postUrl"/>
                <input type="hidden" id="encRequest" name="encRequest" value=$encReq>
                <input type="hidden" name="access_code" id="access_code" value=$xscode>
                <script language='javascript'>document.redirect.submit();</script>
        </form>
        </body>
        </html>
        """
        response_data = Template(html).safe_substitute(
            postUrl=CCAVENUE_URL,
            encReq=encrypted_req,
            xscode=settings.CCAVENUE_ACCESS_CODE,
        )
    else:
        CCAVENUE_URL += f"&encRequest={encrypted_req}"
        CCAVENUE_URL += f"&access_code={settings.CCAVENUE_ACCESS_CODE}"

        response_data = dict()
        response_data["response"] = CCAVENUE_URL

    return response_data


def send_mail_to_user(order_id, decrypted_data):

    txn_status = decrypted_data.get("order_status", 0)
    bank_ref_no = decrypted_data.get("bank_ref_no")
    trans_date = decrypted_data.get("trans_date")
    delivery_name = decrypted_data.get("delivery_name")
    billing_email = decrypted_data.get("billing_email")
    delivery_tel = decrypted_data.get("delivery_tel")
    delivery_address = decrypted_data.get("billing_address")
    mer_amount = decrypted_data.get("mer_amount")
    tracking_id = decrypted_data.get("tracking_id")

    context = {
        "order_id": order_id,
        "bank_ref_no": bank_ref_no,
        "trans_date": trans_date,
        "delivery_name": delivery_name,
        "billing_email": billing_email,
        "delivery_tel": delivery_tel,
        "delivery_address": delivery_address,
        "mer_amount": mer_amount,
        "tracking_id": tracking_id,
    }

    mail_message = ORDER_STATUS_EMAIL_MESSAGE.get(txn_status, "Invalid payment!")

    subject_name = "Payment Status!! "
    subject = subject_name + mail_message

    template = get_template("email.html").render(context)

    send_mail(
        subject,
        None,
        settings.EMAIL_HOST_USER,
        [decrypted_data.get("billing_email")],
        fail_silently=False,
        html_message=template,
    )
