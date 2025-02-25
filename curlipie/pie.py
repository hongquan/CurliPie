import re
import shlex
import logging
from shlex import quote
from collections import deque
from typing import List

import orjson
from first import first
from pydantic import BaseModel, ConfigDict, Field
from pydantic.config import JsonValue
from http_constants.headers import HttpHeaders as HH
from .curly import CURLArgumentParser


REGEX_SINGLE_OPT = re.compile(r'-\w$')
REGEX_SHELL_LINEBREAK = re.compile(r'\\\s+')
logger = logging.getLogger(__name__)
EXAMPLE: JsonValue = {'httpie': 'http -fa admin:xxx quan.hoabinh.vn/api/users name=meow', 'errors': []}


class ConversionResult(BaseModel):
    model_config = ConfigDict(json_schema_extra={'example': EXAMPLE})
    httpie: str
    errors: deque[str] = Field(default_factory=deque)


def join_previous_arg(cmds: deque[str], name: str) -> None:
    prev_arg = cmds[-1]
    if REGEX_SINGLE_OPT.match(prev_arg):
        cmds[-1] += name
    else:
        cmds.append(f'-{name}')


def clean_curl(cmd: str) -> str:
    """Remove slash-escaped newlines and normal newlines from curl command."""
    stripped = REGEX_SHELL_LINEBREAK.sub(' ', cmd)
    return ' '.join(stripped.splitlines())


def curl_to_httpie(cmd: str, long_option: bool = False) -> ConversionResult:
    # The cmd can be multiline string, with escape symbols, shlex doesn't support it, so
    # we should convert it to one-line first.
    oneline = clean_curl(cmd)
    try:
        cargs = shlex.split(oneline)
    except ValueError as e:
        logger.error('Failed to parse as shell command. Error: %s', e)
        return ConversionResult(httpie='', errors=deque([str(e)]))
    if not cargs:
        return ConversionResult(httpie='')
    if cargs[0] == 'curl':
        cargs = cargs[1:]
        if not cargs:
            return ConversionResult(httpie='http')
    args = CURLArgumentParser().parse_args(cargs)
    cmds = deque(['http'])
    if args.verbose:
        cmds.append('--verbose' if long_option else '-v')
    if args.location:
        if long_option:
            cmds.append('--follow')
        else:
            join_previous_arg(cmds, 'F')
    if args.remote_name:
        if long_option:
            cmds.append('--download')
        else:
            join_previous_arg(cmds, 'd')
    if args._data and not args._request_json:
        if long_option:
            cmds.append('--form')
        else:
            join_previous_arg(cmds, 'f')
    if args.proxy:
        cmds.extend(('--proxy', args.proxy))
    user = args.user if args.user else (':'.join(args._auth.get_username_password()) if args._auth else None)
    if user:
        if long_option:
            cmds.extend(('--auth', quote(user)))
        else:
            join_previous_arg(cmds, 'a')
            cmds.append(quote(user))
        
    if args.include:
        cmds.append('--all')
    if args.insecure:
        cmds.extend(('--verify', 'no'))
    elif args.cacert:
        cmds.extend(('--verify', args.cacert))
    if args.cert:
        cmds.extend(('--cert', quote(args.cert)))
    if args.max_redirs:
        cmds.extend(('--max-redirects', str(args.max_redirs)))
    if args.max_time:
        cmds.extend(('--timeout', str(args.max_time)))
    if args.head:
        cmds.append('HEAD')
    elif args.request and not (args._data and args.request == 'POST'):
        cmds.append(args.request)
    # URL
    cmds.append(args._url)
    # Headers
    for k, v in args._headers.to_dict().items():
        cmds.append(f'{quote(k)}:{quote(v)}')
    if args._request_json and not args._data:
        mime = quote(HH.CONTENT_TYPE_VALUES.json)
        key = quote(HH.CONTENT_TYPE)
        cmds.append(f'{key}:{mime}')
    if args.user_agent:
        cmds.append(f'{HH.USER_AGENT}:{quote(args.user_agent)}')
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
            # Strip beginning @
            filepath = v[1:]
            cmds.append(f'{qp}@{quote(filepath)}')
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
        except TypeError:  # v is not string, normally after parsed from JSON
            if isinstance(v, (list, dict)):
                v = quote(orjson.dumps(v).decode())
            cmds.append(f'{qp}:={v}' if not args.get else f'{qp}=={quote(str(v))}')
    if args.data_binary:
        fn = first(v for v in args.data_binary if v and v.startswith('@'))
        if fn:
            # Strip @
            fn = fn[1:]
            cmds.append(f'@{quote(fn)}')
    if args.output:
        param = '-o' if not long_option else '--output'
        cmds.extend((param, quote(args.output)))
    return ConversionResult(httpie=' '.join(cmds), errors=deque(frozenset(args._errors)))
