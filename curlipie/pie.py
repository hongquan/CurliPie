import re
import shlex
import mimetypes
from shlex import quote
from collections import deque
from typing import List

import hh
import orjson
from devtools import debug
from .curly import CURLArgumentParser


REGEX_SINGLE_OPT = re.compile(r'-\w$')


def join_previous_arg(cmds: List[str], name: str):
    prev_arg = cmds[-1]
    if REGEX_SINGLE_OPT.match(prev_arg):
        cmds[-1] += name
    else:
        cmds.append(f'-{name}')


def curl_to_httpie(cmd: str, long_option: bool = False) -> str:
    cargs = shlex.split(cmd)
    debug(cargs)
    if not cargs:
        return ''
    if cargs[0] == 'curl':
        cargs = cargs[1:]
        if not cargs:
            return 'http'
    args = CURLArgumentParser().parse_args(cargs)
    cmds = deque(['http'])
    if args.include or args.verbose:
        cmds.append('--verbose' if long_option else '-v')
    if args.location:
        if long_option:
            cmds.append('--follow')
        else:
            join_previous_arg(cmds, 'F')
    if args.head:
        cmds.append('HEAD')
    elif args.request and not (args._data and args.request == 'POST'):
        cmds.append(args.request)
    if args.user:
        if long_option:
            cmds.extend(('--auth', args.user))
        else:
            join_previous_arg(cmds, 'a')
            cmds.append(args.user)
    if args._data and not args._request_json:
        if long_option:
            cmds.append('--form')
        else:
            join_previous_arg(cmds, 'f')
    # URL
    cmds.append(args._url)
    # Headers
    for k, v in args._headers.items():
        cmds.append(f'{quote(k)}:{quote(v)}')
    if args._request_json and not args._data:
        mime = mimetypes.types_map['.json']
        cmds.append(f'{quote(hh.CONTENT_TYPE)}:{quote(mime)}')
    # Params
    for k, v in args._params:
        if k.startswith('-'):
            cmds.append('--')
        k = k.replace('=', r'\=')
        cmds.append(f'{quote(k)}=={quote(v)}')
    # Data
    for p, v in args._data:
        p = str(p)
        if p.startswith('-'):
            cmds.append('--')
        p = p.replace('=', r'\=')
        qp = quote(p)
        # Syntax for uploading file
        if isinstance(v, str) and v.startswith('@') and not args._request_json:
            cmds.append(f'{qp}@{quote(v)}')
            continue
        # Not uploading file
        # Python shlex's quote will turn bool value to empty string, that is not we want
        if isinstance(v, bool):
            js_bool = str(v).lower()
            cmds.append(f'{qp}:={js_bool}' if not args.get else f'{qp}=={str(v)}')
            continue
        try:
            qv = quote(v)
            cmds.append(f'{qp}={qv}' if not args.get else f'{qp}=={qv}')
        except TypeError:     # v is not string, normally after parsed from JSON
            if isinstance(v, (list, dict)):
                v = quote(orjson.dumps(v).decode())
            debug(v)
            cmds.append(f'{qp}:={v}' if not args.get else f'{qp}=={quote(str(v))}')
    return ' '.join(cmds)
