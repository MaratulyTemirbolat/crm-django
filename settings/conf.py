# Python modules
from decouple import config


# ---------------------------------------
# Environment variables
#
SECRET_KEY = config("CRM_SECRET_KEY", cast=str)
ENV_ID = config("CRM_ENV_ID", cast=str)

# ---------------------------------------
# Django REST Framework settings
#
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ]
}
