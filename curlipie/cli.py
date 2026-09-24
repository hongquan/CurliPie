import sys

import click

from .pie import curl_to_httpie


PROMPT = 'Paste your cURL command (press Enter twice or Ctrl-D when done):'


def _read_interactive() -> str:
    """Prompt the user to paste a cURL command, reading until a blank line or EOF."""
    click.echo(PROMPT, err=True)
    lines: list[str] = []
    try:
        while True:
            line = input()
            if line == '' and lines:
                break
            lines.append(line)
    except EOFError:
        click.echo(err=True)
    except KeyboardInterrupt:
        click.echo(err=True)
    return '\n'.join(lines)


@click.command('curlipie')
@click.argument('curl_command', required=False, default=None)
@click.option(
    '-l',
    '--long',
    'long_option',
    is_flag=True,
    help='Use long-form HTTPie options (e.g. --follow instead of -F).',
)
@click.version_option()
def main(curl_command: str | None, long_option: bool) -> None:
    """Convert a cURL command to an HTTPie command."""
    if curl_command is not None:
        curl_cmd = curl_command.strip()
    elif not sys.stdin.isatty():
        curl_cmd = sys.stdin.read().strip()
    else:
        curl_cmd = _read_interactive().strip()

    if not curl_cmd:
        return

    result = curl_to_httpie(curl_cmd, long_option=long_option)

    if result.errors:
        for err in result.errors:
            click.echo(f'Warning: {err}', err=True)

    click.echo(result.httpie)


if __name__ == '__main__':
    main()
