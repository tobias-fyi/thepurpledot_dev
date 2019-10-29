from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "6hm7o_*8je&#8y6+s+v&id&5w@4#bq-w%@_1bu)g-94$jo0bys"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS = INSTALLED_APPS + ["debug_toolbar"]


try:
    from .local import *
except ImportError:
    pass
