import json

import jwt
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from payment_service.payment_gateway.models import ServiceProvider
from payment_service.payment_gateway.utils import encrypt, generate_random_string
from payment_service.users.models import ApplicationMaster

api_client = APIClient()

# ==========================================================================================
# TEST CASES FOR ccavenue-request
# ==========================================================================================
public_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAysxnaNzYpGXkAVVJZpU0
0I5Mfk4jQwsvbKTrorQAQKePAd5lDsdMxgBq7tCUxxyJNWt249CfDonjoM1butso
qUgSzGFG6jN9EPs3RsbhA0ZE7MxtyHBAGE+O3NcxBXIRZmj0pevTjJYiwSZyuTiT
OlGBIPtTYuXL1Z2FC9jIa3BC0xuk7+yfeOYKMVpzgQPKvQyFIIJyhJ3gKHi460GM
6vku91W8TPetmdUva0Hdh5j5FckC4j8zVOSc2zLdbVd0mHIvb6NZu1t12FYQ3xei
poSuTaWVsBU/PGTQ3nLthMf4cNGrtiU4wmq2g9Uabos6tATsYR9am08zf2fN3Dgg
WwIDAQAB
-----END PUBLIC KEY-----"""

private_key = b"""
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAysxnaNzYpGXkAVVJZpU00I5Mfk4jQwsvbKTrorQAQKePAd5l
DsdMxgBq7tCUxxyJNWt249CfDonjoM1butsoqUgSzGFG6jN9EPs3RsbhA0ZE7Mxt
yHBAGE+O3NcxBXIRZmj0pevTjJYiwSZyuTiTOlGBIPtTYuXL1Z2FC9jIa3BC0xuk
7+yfeOYKMVpzgQPKvQyFIIJyhJ3gKHi460GM6vku91W8TPetmdUva0Hdh5j5FckC
4j8zVOSc2zLdbVd0mHIvb6NZu1t12FYQ3xeipoSuTaWVsBU/PGTQ3nLthMf4cNGr
tiU4wmq2g9Uabos6tATsYR9am08zf2fN3DggWwIDAQABAoIBAEGApCYKry7qeiq0
EXFA4D48uBhTxK/y/O5qlnGHEk3P0TEZVCrh1LpfiCp61JM7dFX8z/nleHqJryxR
KD/Cae/Dh87b3LvoxYyml8QUmLkmCT0zCoKjPxCbIdnS59KKdXROkjbFZR8Tn0Yj
1Qpea696g+rTQqu+7YehyUd6TcHlfXjd4urX9uXKJdsnCgo+/VwXxSWCaTB0M/eb
BodyK+bHRwCrvPsUBvBKHgqwl050NGlfxm8I5teYQzzPc4v0bNhuENZiapIR07Mv
2dsHptDiMhOu9JeiMHRfd+jUkALwl1uwPEJscMUMaWKxs2ovTB1MsDUH/pfqHX+R
AGUtVgECgYEA6AhFMJmTWSPy9MbjdhZ8PFv+sSKBgFuVCaoRN75u0rySIiApBGZa
5P+LtfQrZq581KD/CYHQElIwfdU9KM0cLq6bscY/6mgef5rojNnKUrMT9DwOoPLz
Xnb6DemilpO/R5VLQydXnMTjGqnH06UHhywpdPIi+KlDgFotxWVETmsCgYEA378X
ImGiM/n9+OhG8G+lEdMoIQm3PQKPREI89Q0tcCf6hhGUE1f9s9iUxBkQP4TMYsrY
fSoRmPltK1iNNiH5LuzNSMhPGxk7WBcSacRElR7eZ8KhHIUhAZY0PVdZCXNyBgrX
MfVyPShTxRP3uWOB4jSLxlxPiyl5isfI1hR9EdECgYEA3l7OsHz+Ufe56AyUAaAb
AF3KAUjog3NBqjlqttmyrBQ8mKfpp2XQxpaB9qdC0O14hO6mfR4DowtRnca3DltE
HxkH7Z/psWSHlhOHuzUeSZOGFBNakbVEt8ueaab3Qwfl0Vyq/Hi/5mZqoCsGbzdB
t7IDKSjFiznsjx3dr8gVZnECgYAco/RNJVxC9PwqkWkLO+9QUcwwNnMrLxmxrhzp
bU9krOlnofZnZ3sFO3MHiwHGb7RN7RM7KlhoUX1E8CfbRwwDkrJQX7uoh1lOVF26
BjKVOAdWFtbStMPd1SFIvNab3Bg7Z8XWEkoWRAQ9FOo/49nrX7iIoqZX9O4m8p3l
sWe1EQKBgQCqFhS5pNKakZSEkxWrSzCEaIscm7jtdpID3UVw7DJDOoGPBdFeqIye
oABa0TSTMutG1rb8RAohtJ6Y8bDsKNq4acS1YYeRb7iqzvhtL3Skxt1JvgUUgD02
4eO0suGzTJQxqDVqZo7e4yGuED6v8Zonf+m+edUc5UrE3ieJfpNiBg==
-----END RSA PRIVATE KEY-----"""

d_dict = {
    "response_type": "JSON",
    "currency": "INR",
    "amount": 100.00,
    "language": "EN",
    "billing_name": "Peter",
    "billing_address": "Santacruz",
    "billing_city": "Mumbai",
    "billing_state": "MH",
    "billing_zip": "400054",
    "billing_country": "India",
    "billing_tel": "0229874789",
    "billing_email": "abc@gmail.com",
    "delivery_name": "Parth",
    "delivery_address": "pb offict",
    "delivery_city": "Mumbai",
    "delivery_state": "Maharashtra",
    "delivery_zip": "400038",
    "delivery_country": "India",
    "delivery_tel": "0221234321",
    "merchant_param1": "additionalInfo.",
    "merchant_param2": "additional-Info.",
    "merchant_param3": "additionalInfo.",
    "merchant_param4": "additional)Info",
    "merchant_param5": "additional/Info",
}


def test_ccavenue_request_success(db):
    working_key = generate_random_string(32)
    access_code = generate_random_string(18)

    ApplicationMaster.objects.create(
        name="abc",
        application_config={"app_config1": "0001"},
        working_key=working_key,
        access_code=access_code,
        redirect_url="http://localhost:8000/payment/store01_payment_response",
        cancel_url="http://localhost:8000/payment/store01_payment_response",
        public_key=public_key
    )

    service_provider = ServiceProvider.objects.create(
        name="abc",
        business_name="abc",
        contact_person_name="abc",
        contact_person_email="abc@test.com",
        contact_person_phone="5577889966",
        working_key="abc",
        access_code="abc",
    )

    d_dict['service_provider_id'] = service_provider.id
    json_payload = json.dumps(d_dict)
    generate_app_request = encrypt(json_payload, working_key)
    data_to_post = {
        "app_request": generate_app_request,
        "app_id": access_code,
    }

    auth_headers = {
        "id": access_code
    }
    encoded_app_id = jwt.encode(auth_headers, private_key, algorithm="RS256")

    url = reverse("payment_gateway:ccavenue-request")
    response = api_client.post(url, data=data_to_post, HTTP_AUTHORIZATION=f'bearer {encoded_app_id}', format="json")

    assert response.status_code == status.HTTP_200_OK


def test_ccavenue_app_request_key_invalid_error(db):
    working_key = generate_random_string(32)
    access_code = generate_random_string(18)

    json_payload = json.dumps(d_dict)
    generate_app_request = encrypt(json_payload, working_key)

    ApplicationMaster.objects.create(
        name="abc",
        application_config={"app_config1": "0001"},
        working_key=working_key,
        access_code=access_code,
        redirect_url="http://localhost:8000/payment/store01_payment_response",
        cancel_url="http://localhost:8000/payment/store01_payment_response",
        public_key=public_key
    )
    auth_headers = {
        "id": access_code
    }

    data_to_post = {
        "app_request": generate_app_request
    }

    encoded_app_id = jwt.encode(auth_headers, private_key, algorithm="RS256")

    url = reverse("payment_gateway:ccavenue-request")
    response = api_client.post(url, data_to_post, HTTP_AUTHORIZATION=f'bearer {encoded_app_id}',
                               format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


ccavenue_request_payload = {
    "app_id": "abc",
    "app_request":
        "3d19f65b8d8a2910a9db5c75f6e94bc3524bf463c7aff523a36b6d80a0faeab48092294b7a63d948cf92fe985882f8d41f0acde263479b"
        "704b4e8b9c0e6cd8b89137408d500c0ffc4e8abd27c3e87eca746e8a558932756619ff7e4255eb806e1e877f9ede5fbc9eecd750cb2419"
        "1f80bf6c91d661e22a33a5fc6d4730df1d5f2a425f5fb0d838b3d74d10bf274e61a77272470cd211c55a8474a2f14952365349f1ecbe"
        "cddf40c1491bc5b76d30a52f177105fb9b121abfd9ce25efcf84854c706b460b34af0eb0dd65b0ab11e006b5596d79d783af12642ad1b"
        "bbb4b05b9adecc2308a9fd17f9566a8f2cc30026a5c89aa2b3f394678e61b11fd14bfd3ddfc76f29e4562eb0a25f457a16d79c7060e08c"
        "298482ccc7f9f7bebe6344a64db1a7b39af600b5ddd2070a91dc49ebf0974e80f44d05386e8a6f0dac4746880f6013184a4ee2f569d33d"
        "4be998add526317884e4cb0dca2014823e78b461d8c5837e237218582ef920a02454d1485f0e53e2287d8036a0acf70f6d68beff998a92"
        "c40cc41f8b59a444378795fcf1a3d13f5911ab3d6f2b0db381cd1268661c6b98b5a53a4646e9e1504a1adc9a77e253399fb80ebccd1457"
        "0cc23504d1f74ea5c33cca17898a26d1ab3c5898a09c5588e793fb091209281007028ff0816f651d741cab4723b24be9df5494e8d8c9f9"
        "cadcdacebcbe8df04d04a809555ad141423a3fcc29b1ac2650f64418908be28ceb11c861692bdb972878a2c4472b03d47cb3a440af70d1"
        "2d8efbd764641d2c870260a50aea50666fb0bf1ab9cf8807bb67be6cf2d6c9c53ebc1e587d58becb582798e823cf00530fa606898fa93f"
        "c7a1f0ac7ff50b6303758928c9ad9cd51c18eb7a783f340f4ed035a9364aa14ad62bac4585f054be025adc67df4ad0f505e5c5956c9e7b"
        "3df40a8c6bf933385e6715332bf972f4c36adc40ace7e9968852871f8e2e9baf96416ea7b7b5e45fc69cc76cae17a07e28e219793d538c"
        "6b126f1f8482f1bc930d857dd54f0a5a49974c9645660"
}


def test_ccavenue_request_app_id_not_found(db):
    working_key = generate_random_string(32)
    access_code = generate_random_string(18)
    ApplicationMaster.objects.create(
        name="abc",
        application_config={"app_config1": "0001"},
        working_key=working_key,
        access_code=access_code,
        redirect_url="http://localhost:8000/payment/store01_payment_response",
        cancel_url="http://localhost:8000/payment/store01_payment_response",
        public_key=public_key,
    )

    auth_headers = {
        "id": access_code
    }

    encoded_app_id = jwt.encode(auth_headers, private_key, algorithm="RS256")

    url = reverse("payment_gateway:ccavenue-request")

    response = api_client.post(url, ccavenue_request_payload, HTTP_AUTHORIZATION=f'bearer {encoded_app_id}',
                               format="json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_ccavenue_request_api_failed(db):
    url = reverse("payment_gateway:ccavenue-request")
    response = api_client.post(url, ccavenue_request_payload, format="json")

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data["detail"] == "Authentication credentials were not provided."


# ==========================================================================================
# TEST CASES FOR ccavenue-payment-status
# ==========================================================================================
def test_payment_status_api_failed_400(db):
    """
    order_no or reference_no is not passed in params
    """
    url = reverse("payment_gateway:ccavenue-payment-status")
    response = api_client.get(url, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_payment_status_api_failed_405(db):
    """
    Method not allowed
    """
    url = reverse("payment_gateway:ccavenue-payment-status")
    response = api_client.post(url, format="json")

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_payment_status_api_404(db):
    """
    order does not exist in CCAvenue
    """
    url = reverse("payment_gateway:ccavenue-payment-status") + "?order_no=X0x0x0x"

    response = api_client.get(url, format="json")

    assert response.status_code == status.HTTP_404_NOT_FOUND

# ==========================================================================================
# TEST CASES FOR ccavenue-response
# ==========================================================================================
