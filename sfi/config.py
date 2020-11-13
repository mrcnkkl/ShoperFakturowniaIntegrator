import os
import logging


class ConfigBase:
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    SECRET_KEY = os.getenv("SMTP_SERVER") or "very_very_secret_key_to_be_changed_in_production"
    log_level = logging.DEBUG
