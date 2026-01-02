# store/utils/imagekit.py
import os
from imagekitio import ImageKit
from django.conf import settings

def get_imagekit():
    # Lazy load keys from settings
    private_key = getattr(settings, "IMAGEKIT_PRIVATE_KEY", None)
    public_key = getattr(settings, "IMAGEKIT_PUBLIC_KEY", None)
    url_endpoint = getattr(settings, "IMAGEKIT_URL_ENDPOINT", None)

    # If any key is missing, you can either raise an error or return None
    if not all([private_key, public_key, url_endpoint]):
        raise RuntimeError(
            "ImageKit is not configured. "
            "Set IMAGEKIT_PRIVATE_KEY, IMAGEKIT_PUBLIC_KEY, IMAGEKIT_URL_ENDPOINT"
        )

    # ✅ Return proper ImageKit instance
    return ImageKit(
        private_key=private_key,
    )
