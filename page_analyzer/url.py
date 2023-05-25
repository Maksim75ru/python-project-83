import validators
from urllib.parse import urlparse

MAX_URL_LEN = 255


def normalize_url(url: str) -> str:
    """

    Args:
        url: string url

    Returns: <protocol>://<domain name> structure

    """
    parsed_url = urlparse(url, allow_fragments=True)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def validate_url(url: str) -> dict:
    """

    Args:
        url: string url

    Returns: blank dict or dict where key = url, value = Error message

    """
    errors = {}
    if len(url) == 0:
        errors['url'] = 'No url'

    if errors or not validators.url(url) or len(url) > MAX_URL_LEN:
        errors["url"] = "Not valid url"

    return errors
