from pathlib import Path

from single_version import get_version

from .pie import curl_to_httpie, ConversionResult   # NOQA


__version__ = get_version('curlipie', Path(__file__).parent.parent)
