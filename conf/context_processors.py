
"""Context processor file."""

from django.conf import settings


def global_vars(request):
    return {
        'GOOGLE_TAG_MANAGER_ID': settings.GOOGLE_TAG_MANAGER_ID,
        'DEBUG': settings.DEBUG
    }
