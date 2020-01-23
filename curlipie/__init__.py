from pathlib import Path

from .ver import get_version
from .pie import curl_to_httpie   # NOQA


__version__ = get_version('curlipie', Path(__file__).parent.parent)
