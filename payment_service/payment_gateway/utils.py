import hashlib
from binascii import hexlify, unhexlify
from string import Template

from Crypto.Cipher import AES
from django.conf import settings

from payment_service.common.exceptions import DecryptionFailed


def generate_obj_id():
    """
    return object id
    """
    from bson import ObjectId

    oid = ObjectId()
    oid_str = str(oid)
    return oid_str


def generate_random_string(string_size=18):
    """
    Creates random string based on string_size.
    :param string_size:  an integer argument which determines string length
    :return: 'str': alphanumeric string of particular string length determined by the string_size parameter
    """
    import random
    import string

    alphanumeric_characters = string.ascii_uppercase + string.digits

    return "".join(
        random.SystemRandom().choice(alphanumeric_characters)
        for _ in range(string_size)
    )


def pad(data):
    """
    ccavenue method to pad data.
    :param data: plain text
    :return: padded data.
    """
    length = 16 - (len(data) % 16)
    data += chr(length) * length
    return data


def unpad(data):
    """
    ccavenue method to unpad data.
    :param data: encrypted data
    :return: plain data
    """
    return data[0: -ord(data[-1])]


def encrypt(plain_text, working_key):
    """
    Method to encrypt cc-avenue hash.
    :param plain_text: plain text
    :param working_key: cc-avenue working key.
    :return: md5 hash
    """

    iv = "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
    plain_text = pad(plain_text)

    byte_array_wk = bytearray()
    byte_array_wk.extend(map(ord, working_key))

    enc_cipher = AES.new(hashlib.md5(byte_array_wk).digest(), AES.MODE_CBC, iv)
    hexl = hexlify(enc_cipher.encrypt(plain_text)).decode("utf-8")

    return hexl


def decrypt(cipherText, workingKey):
    iv = "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"

    try:
        encryptedText = unhexlify(cipherText)
        bytearrayWorkingKey = bytearray()
        bytearrayWorkingKey.extend(map(ord, workingKey))
        decCipher = AES.new(hashlib.md5(bytearrayWorkingKey).digest(), AES.MODE_CBC, iv)
    except Exception as e:
        print("Invalid Encryption / Algorithm", e)
        raise DecryptionFailed()
    return unpad(decCipher.decrypt(encryptedText).decode("utf-8"))


def get_decrypted_response_html(plain_text):
    data = "<table border=1 cellspacing=2 cellpadding=2><tr><td>"
    data = data + plain_text.replace("=", "</td><td>")
    data = data.replace("&", "</td></tr><tr><td>")
    data = data + "</td></tr></table>"

    html = """\
        <html>
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
                <title>Response Handler</title>
            </head>
            <body>
                <center>
                    <font size="4" color="blue"><b>Response Page</b></font>
                    <br>
                    $response
                </center>
                <br>
            </body>
        </html>
        """

    fin = Template(html).safe_substitute(response=data)
    return fin


def res(enc_resp):
    """
    Please put in the 32 bit alphanumeric key in quotes provided by CCAvenues.
    """

    dec_resp = decrypt(enc_resp, settings.CCAVENUE_WORKING_KEY)

    decrypted_data = dict(item.split("=") for item in dec_resp.split("&") if item)

    fin = get_decrypted_response_html(dec_resp)

    return fin, decrypted_data
