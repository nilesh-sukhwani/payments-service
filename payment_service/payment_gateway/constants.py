# Django

"""
ORDER STATUS CONSTANT START
'order_status'
"""
PENDING = 0
SUCCESS = 1
FAILURE = 2
ABORTED = 3
INVALID = 4
TIMEOUT = 5
"""
ORDER STATUS CONSTANT END--
"""

"""
ORDER STATUS EMAIL MESSAGE CONSTANT START
"""
ORDER_STATUS_EMAIL_MESSAGE = {
    # "Pending": 0,
    "Success": "Your Payment Successfully Done!!",
    "Failure": "Your Payment Failed!!",
    "Aborted": "Your payment is Aborted!!",
    "Invalid": "Invalid payment!",
    "Timeout": "Payment Timeout!",
}
"""
ORDER STATUS EMAIL MESSAGE CONSTANT END--
"""


"""
ORDER STATUS CONSTANT START
"""
ORDER_STATUS_CHOICES = [
    (0, "Pending"),
    (1, "Success"),
    (2, "Failure"),
    (3, "Aborted"),
    (4, "Invalid"),
    (5, "Timeout"),
]
ORDER_STATUS = {
    "Pending": 0,
    "Success": 1,
    "Failure": 2,
    "Aborted": 3,
    "Invalid": 4,
    "Timeout": 5,
}
"""
ORDER STATUS CONSTANT END
"""


"""
PAYMENT_MODE CONSTANT START
"""
PAYMENT_MODE_CHOICES = [
    (1, "IVR"),
    (2, "S"),
    (3, "EMI"),
    (4, "Credit Card"),
    (5, "Net banking"),
    (6, "Debit Card"),
    (7, "Cash Card"),
    (8, "UPI"),
    (9, "Wallet"),
]

PAYMENT_MODE_DICT = {
    "IVR": 1,
    "S": 2,
    "EMI": 3,
    "Credit Card": 4,
    "Net banking": 5,
    "Debit Card": 6,
    "Cash Card": 7,
    "UPI": 8,
    "Wallet": 9,
}
"""
PAYMENT_MODE CONSTANT END
"""


"""
CCAVENUE ORDER GET_STATUS CONSTANT START
"""
GET_ORDER_STATUS = "orderStatusTracker"
RESPONSE_TYPE = "JSON"
REQUEST_TYPE = "JSON"
VERSION = "1.2"
"""
ORDER STATUS EMAIL MESSAGE CONSTANT END--
"""

"""
Notifications Constants Start.
"""
MAIL_NOTIFICATION_RETRIES = 3
MAIL_NOTIFICATION_RETRY_DELAY = 30
"""
Notifications Constants End.
"""


"""
CCAvenue Response Status Constants Start.
"""
CCAVENUE_SUCCESS_STATUS = 0
CCAVENUE_FAILED_STATUS = 1
"""
CCAvenue Response Status Constants End.
"""
