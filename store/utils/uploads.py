# store/utils/uploads.py
from store.utils.imagekit import get_imagekit


def upload_profile_image(file, username):
    """
    Upload staff profile image to ImageKit
    """
    imagekit = get_imagekit()  # lazy load

    response = imagekit.files.upload(
        file=file.read(),  # convert Django file → bytes
        file_name=f"staff_{username}.jpg",
        folder="/profiles",
    )

    return response.url
