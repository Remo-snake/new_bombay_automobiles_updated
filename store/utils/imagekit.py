# store/utils/imagekit.py
import os
from django.conf import settings
from imagekitio import ImageKit

def get_imagekit():
    private_key = getattr(settings, "IMAGEKIT_PRIVATE_KEY", None)
    public_key = getattr(settings, "IMAGEKIT_PUBLIC_KEY", None)
    url_endpoint = getattr(settings, "IMAGEKIT_URL_ENDPOINT", None)

    if not (private_key and public_key and url_endpoint):
        # Optional: you can just return None for local dev
        raise RuntimeError(
            "ImageKit is not configured. "
            "Set IMAGEKIT_PRIVATE_KEY, IMAGEKIT_PUBLIC_KEY, IMAGEKIT_URL_ENDPOINT"
        )

    return ImageKit(
        private_key=private_key,

    )
