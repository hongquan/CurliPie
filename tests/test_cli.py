import sys
import builtins
from io import StringIO
from unittest.mock import patch, MagicMock, call

import pytest

from curlipie.cli import main


def _stdin_mock(text: str) -> MagicMock:
    """Return a mock that looks like a non-TTY stdin with the given text."""
    mock = MagicMock(spec=StringIO)
    mock.read.return_value = text
    mock.isatty.return_value = False
    return mock


def run_cli(*argv: str, stdin: str | None = None) -> tuple[str, str, int]:
    """Run main() with the given argv, return (stdout, stderr, exit_code).

    When *stdin* is given the mock stdin reports isatty()=False (pipe mode).
    When *stdin* is None the mock stdin reports isatty()=True (interactive).
    """
    tty_mock = MagicMock()
    tty_mock.isatty.return_value = True

    stdin_mock = _stdin_mock(stdin) if stdin is not None else tty_mock

    with (
        patch('sys.argv', ['curlipie', *argv]),
        patch('sys.stdin', stdin_mock),
        patch('sys.stdout', new_callable=StringIO) as mock_out,
        patch('sys.stderr', new_callable=StringIO) as mock_err,
    ):
        try:
            main()
            code = 0
        except SystemExit as e:
            code = e.code if isinstance(e.code, int) else 1
        return mock_out.getvalue().strip(), mock_err.getvalue().strip(), code


def test_simple_get():
    stdout, _, code = run_cli('curl http://example.com')
    assert code == 0
    assert stdout == 'http example.com'


def test_post_form():
    stdout, _, code = run_cli("curl -X POST http://example.com -d 'name=admin&size=12'")
    assert code == 0
    assert stdout == 'http -f example.com name=admin size=12'


def test_long_options():
    stdout, _, code = run_cli('--long', 'curl -L http://example.com')
    assert code == 0
    assert '--follow' in stdout
    assert '-F' not in stdout


def test_stdin_input():
    stdout, _, code = run_cli(stdin='curl http://example.com')
    assert code == 0
    assert stdout == 'http example.com'


def test_no_input_exits_ok():
    # Running interactively with no input (immediate Ctrl-D) exits 0 silently.
    with patch('builtins.input', side_effect=EOFError):
        _, _, code = run_cli()
    assert code == 0


def test_ctrl_c_exits_ok():
    # Ctrl-C during interactive input exits 0 without a traceback.
    with patch('builtins.input', side_effect=KeyboardInterrupt):
        _, _, code = run_cli()
    assert code == 0


def test_empty_stdin_exits_ok():
    # Piping empty input exits 0 silently.
    _, _, code = run_cli(stdin='')
    assert code == 0


def test_interactive_single_line():
    # User pastes a single-line curl then hits Enter twice.
    inputs = iter(['curl http://example.com', ''])
    with patch('builtins.input', side_effect=inputs):
        stdout, _, code = run_cli()
    assert code == 0
    assert stdout == 'http example.com'


def test_interactive_multiline_curl():
    # User pastes a backslash-continued curl command, then a blank line.
    inputs = iter([
        "curl -X POST \\",
        "  https://example.com/api \\",
        "  -H 'Content-Type: application/json' \\",
        "  -d '{ \"name\": \"bob\" }'",
        '',
    ])
    with patch('builtins.input', side_effect=inputs):
        stdout, _, code = run_cli()
    assert code == 0
    assert 'example.com/api' in stdout
    assert 'name=bob' in stdout


def test_warnings_go_to_stderr():
    # A parse error (unterminated quote) should print a warning to stderr
    # and still exit cleanly (exit 0), printing whatever httpie output exists.
    stdout, stderr, code = run_cli("curl 'unterminated")
    assert code == 0
    assert 'Warning' in stderr


def test_pipe_multiline_curl():
    curl = (
        "curl -X POST \\\n"
        "http://example.com/api \\\n"
        "-H 'Content-Type: application/json' \\\n"
        "-d '{\"name\": \"bob\"}'"
    )
    stdout, _, code = run_cli(stdin=curl)
    assert code == 0
    assert 'example.com/api' in stdout
    assert 'name=bob' in stdout
