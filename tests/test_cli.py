from click.testing import CliRunner
from pytest_mock import MockerFixture

from curlipie.cli import main


runner = CliRunner()


def test_simple_get() -> None:
    result = runner.invoke(main, ['curl http://example.com'])
    assert result.exit_code == 0
    assert result.output.strip() == 'http example.com'


def test_post_form() -> None:
    result = runner.invoke(main, ["curl -X POST http://example.com -d 'name=admin&size=12'"])
    assert result.exit_code == 0
    assert result.output.strip() == 'http -f example.com name=admin size=12'


def test_long_options() -> None:
    result = runner.invoke(main, ['--long', 'curl -L http://example.com'])
    assert result.exit_code == 0
    assert '--follow' in result.output
    assert '-F' not in result.output


def test_stdin_input() -> None:
    result = runner.invoke(main, input='curl http://example.com')
    assert result.exit_code == 0
    assert result.output.strip() == 'http example.com'


def test_empty_stdin_exits_ok() -> None:
    # Piping empty input exits 0 silently.
    result = runner.invoke(main, input='')
    assert result.exit_code == 0


def test_warnings_go_to_stderr() -> None:
    # A parse error (unterminated quote) should print a warning to stderr
    # and still exit cleanly (exit 0), printing whatever httpie output exists.
    result = runner.invoke(main, ["curl 'unterminated"])
    assert result.exit_code == 0
    assert 'Warning' in result.output


def test_pipe_multiline_curl() -> None:
    curl = (
        'curl -X POST \\\nhttp://example.com/api \\\n-H \'Content-Type: application/json\' \\\n-d \'{"name": "bob"}\''
    )
    result = runner.invoke(main, input=curl)
    assert result.exit_code == 0
    assert 'example.com/api' in result.output
    assert 'name=bob' in result.output


def test_interactive_input(mocker: MockerFixture) -> None:
    # When stdin looks like a TTY, the CLI prompts and reads interactive input.
    stdin = mocker.patch('curlipie.cli.sys.stdin')
    stdin.isatty.return_value = True
    stdin.read.return_value = ''

    result = runner.invoke(main, input='curl http://example.com\n')
    assert result.exit_code == 0
    assert result.output.strip() == 'http example.com'
