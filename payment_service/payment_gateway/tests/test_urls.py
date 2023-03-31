from django.urls import resolve, reverse


def test_ccavenue_request():
    assert reverse("payment_gateway:ccavenue-request") == "/payment/request"

    assert resolve("/payment/request").view_name == "payment_gateway:ccavenue-request"


def test_ccavenue_response():
    assert reverse("payment_gateway:ccavenue-response") == "/payment/response"

    assert resolve("/payment/response").view_name == "payment_gateway:ccavenue-response"


def test_ccavenue_payment_cancel():
    assert reverse("payment_gateway:ccavenue-cancel") == "/payment/cancel"

    assert (
        resolve("/payment/cancel").view_name
        == "payment_gateway:ccavenue-cancel"
    )


def test_ccavenue_payment_status():
    assert reverse("payment_gateway:ccavenue-payment-status") == "/payment/status"

    assert (
        resolve("/payment/status").view_name
        == "payment_gateway:ccavenue-payment-status"
    )
