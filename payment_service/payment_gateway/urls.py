from django.urls import path

from payment_service.payment_gateway import views

ccavenue_urls = [
    path("request", views.CCAvenueRequestView.as_view(), name="ccavenue-request"),
    path("response", views.CCAvenueResponseView.as_view(), name="ccavenue-response"),
    path("cancel", views.CCAvenuePaymentCancelView.as_view(), name="ccavenue-cancel"),
    path("status", views.order_status_view, name="ccavenue-payment-status"),
]

testing_urls = [
    path("request_form", views.webprint, name="ccavenue-request-form"),
    path(
        "test_request", views.TestCCAvenuePaymentRequest.as_view(), name="test-request"
    ),
    path(
        "store01_payment_response",
        views.get_encrypted_payment_response,
        name="payment-response",
    ),
    # for encrypting and decrypting sample payload.
    path("get/encryption", views.get_encrypted_data, name="test-encryption"),
    path("get/decryption", views.get_decrypted_data, name="test-decryption"),
]

urlpatterns = ccavenue_urls + testing_urls
