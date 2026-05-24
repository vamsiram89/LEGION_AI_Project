"""
Notification utilities.

In production you would integrate with Twilio, WhatsApp, email or push
services (Firebase) to send alerts.  The functions here are placeholders
that log messages to the console.  They return a boolean indicating
success.
"""

import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def send_alert(contact: dict, message: str) -> bool:
    """
    Send an alert message to a contact.  The contact dict should contain
    'name', 'phone' and/or 'email'.  This function currently logs the
    message; integrate with a messaging service for real use.
    """
    logger.info(f"Sending alert to {contact.get('name')} ({contact.get('phone') or contact.get('email')}): {message}")
    # Here you would call Twilio or another service
    return True