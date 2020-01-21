import shlex
import mimetypes
from shlex import quote
from collections import deque

import hh
from .curly import CURLArgumentParser


def curl_to_httpie(cmd: str, long_option: bool = False) -> str:
    cargs = shlex.split(cmd)
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
    if args.head:
        cmds.append('HEAD')
    elif args.request and not (args._data and args.request == 'POST'):
        cmds.append(args.request)
    if args.user:
        if long_option:
            cmds.extend(('--auth', args.user))
        else:
            cmds.extend(('-a', args.user))
    if args._data and not args._request_json:
        cmds.append('--form' if long_option else '-f')
    # URL
    cmds.append(args._url)
    # Headers
    for k, v in args._headers.items():
        cmds.append(f'{k}:{v}')
    if args._request_json and not args._data:
        mime = mimetypes.types_map['.json']
        cmds.append(f'{hh.CONTENT_TYPE}:{mime}')
    # Params
    for k, v in args._params:
        cmds.append(f'{k}=={v}')
    # Data
    for p, v in args._data:
        cmds.append(f'{p}={v}')
    return ' '.join(quote(p) for p in cmds)
