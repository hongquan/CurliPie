import sys
import argparse

from .pie import curl_to_httpie


def _read_interactive() -> str:
    """Prompt the user to paste a cURL command, reading until a blank line or EOF."""
    print('Paste your cURL command (press Enter twice or Ctrl-D when done):', file=sys.stderr)
    lines: list[str] = []
    try:
        while True:
            line = input()
            if line == '' and lines:
                break
            lines.append(line)
    except (EOFError, KeyboardInterrupt):
        print(file=sys.stderr)  # newline after ^C so the shell prompt appears on its own line
    return '\n'.join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog='curlipie',
        description='Convert a cURL command to an HTTPie command.',
    )
    parser.add_argument(
        'curl',
        nargs='?',
        metavar='CURL_COMMAND',
        help='cURL command to convert. Reads from stdin when omitted.',
    )
    parser.add_argument(
        '-l',
        '--long',
        action='store_true',
        default=False,
        help='Use long-form HTTPie options (e.g. --follow instead of -F).',
    )
    args = parser.parse_args()

    if args.curl is not None:
        curl_cmd = args.curl.strip()
    elif not sys.stdin.isatty():
        curl_cmd = sys.stdin.read().strip()
    else:
        curl_cmd = _read_interactive().strip()

    if not curl_cmd:
        sys.exit(0)

    result = curl_to_httpie(curl_cmd, long_option=args.long)

    if result.errors:
        for err in result.errors:
            print(f'Warning: {err}', file=sys.stderr)

    print(result.httpie)


if __name__ == '__main__':
    main()
