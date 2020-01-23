import re
import sys
from pathlib import Path

from first import first


_REGEX_VERSION = re.compile(r'\s*version\s*=\s*["\']([.0-9a-z]+)["\']\s*$')

pyver = sys.version_info[:2]
if pyver <= (3, 7):
    import importlib_metadata
else:
    import importlib.metadata as importlib_metadata


def get_version(package: str, looked_path: Path):
    # Poetry don't include pyproject.toml file to distribution package,
    # so, if we see that file, its mean that the package is imported from development folder
    filepath = looked_path / 'pyproject.toml'   # type: Path
    if filepath.exists():
        found = first(_REGEX_VERSION.match(line) for line in filepath.open())
        if not found:
            return '0.0'
        return found.group(1)
    try:
        return importlib_metadata.version(package)
    except importlib_metadata.PackageNotFoundError:
        pass
    return '0.0'
