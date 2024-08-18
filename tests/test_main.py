#
# Copyright (C) 2020-2024 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for password_trainer.main module
"""
import os
import signal
from unittest.mock import patch

import pytest

from password_trainer.main import main, PasswordTrainerScript, HINT_MESSAGE

from .constants import MESSAGE
from .helpers import (
    add_getpass_mock,
    mock_stdin_password_file,
    mock_stdin_password_file_binary,
)

COMMAND = 'password-trainer'


def test_main_script_exit_code_no_message(capsys, env_debug_disabled) -> None:
    """
    Test PasswordTrainerScript object exit method with specified
    code and without as message
    """
    script = PasswordTrainerScript()
    code = 254
    with pytest.raises(SystemExit) as exit_status:
        script.exit(code)
    assert exit_status.value.code == code
    captured = capsys.readouterr()
    assert captured.err == ''
    assert captured.out == ''


def test_main_script_signal_handler() -> None:
    """
    Test raising the signal handler of PasswordTrainerScript to
    """
    script = PasswordTrainerScript()
    with pytest.raises(SystemExit) as exit_status:
        with patch.object(script, '__SIGINT__') as signal_handler:
            os.kill(os.getpid(), signal.SIGINT)
        assert signal_handler.called
    assert exit_status.value.code == 0


def test_main_script_exit_code_with_message(capsys, env_debug_disabled) -> None:
    """
    Test PasswordTrainerScript object exit method with specified
    code and message
    """
    script = PasswordTrainerScript()
    code = 254
    with pytest.raises(SystemExit) as exit_status:
        script.exit(code, MESSAGE)
    assert exit_status.value.code == code
    captured = capsys.readouterr()
    assert captured.err.splitlines() == [MESSAGE]
    assert captured.out == ''


def test_main_run_help(capsys, monkeypatch) -> None:
    """
    Test running CLI entrypoint with --help
    """
    monkeypatch.setattr('sys.argv', [COMMAND, '--help'])
    with pytest.raises(SystemExit) as exit_status:
        main()
    captured = capsys.readouterr()
    assert captured.err == ''
    assert captured.out.splitlines()
    assert exit_status.value.code == 0


def test_main_run_debug(capsys, monkeypatch, mock_getpass) -> None:
    """
    Test running CLI entrypoint with no command line arguments, guessing
    the mocked password 100% right with mocked getpass input
    """
    monkeypatch.setattr('sys.argv', [COMMAND, '--debug'])
    with pytest.raises(SystemExit) as exit_status:
        main()
    assert exit_status.value.code == 0
    captured = capsys.readouterr()
    assert captured.err == ''
    assert captured.out.splitlines() == ['Total 5 attempts, 5 answers (100%)']


def test_main_run_no_args(capsys, monkeypatch, mock_getpass) -> None:
    """
    Test running CLI entrypoint with no command line arguments, guessing
    the mocked password 100% right with mocked getpass input
    """
    monkeypatch.setattr('sys.argv', [COMMAND])
    with pytest.raises(SystemExit) as exit_status:
        main()
    assert exit_status.value.code == 0
    captured = capsys.readouterr()
    assert captured.err == ''
    assert captured.out.splitlines() == ['Total 5 attempts, 5 answers (100%)']


def test_main_run_no_input(capsys, monkeypatch, mock_getpass) -> None:
    """
    Test running CLI entrypoint with no command line arguments and not input
    for password to train given
    """
    monkeypatch.setattr('sys.argv', [COMMAND])
    add_getpass_mock(monkeypatch, '')
    with pytest.raises(SystemExit) as exit_status:
        main()
    assert exit_status.value.code == 1


def test_main_run_stdin_password(capsys, monkeypatch, mock_getpass) -> None:
    """
    Test running CLI entrypoint with no command line arguments and password as
    input from stdin
    """
    password = 'InvisiblerandomGeneratedPassword'
    monkeypatch.setattr('sys.argv', [COMMAND, '--file=-'])
    mock_stdin_password_file(monkeypatch, password)
    with pytest.raises(SystemExit) as exit_status:
        main()
    assert exit_status.value.code == 0
    captured = capsys.readouterr()
    assert password not in captured.out.splitlines()


def test_main_run_stdin_password_show_password(capsys, monkeypatch, mock_getpass) -> None:
    """
    Test running CLI entrypoint with no command line arguments and password as
    input from stdin and show the generated password in output
    """
    password = 'randomGeneratedPassword'
    expected_line = f'{HINT_MESSAGE}{password}'
    monkeypatch.setattr('sys.argv', [COMMAND, '--show-password', '--file=-'])
    mock_stdin_password_file(monkeypatch, password)
    with pytest.raises(SystemExit) as exit_status:
        main()
    assert exit_status.value.code == 0
    captured = capsys.readouterr()
    assert expected_line in captured.out.splitlines()


def test_main_run_stdin_password_unicode_error(capsys, monkeypatch, mock_getpass) -> None:
    """
    Test running CLI entrypoint with no command line arguments and password as
    input from stdin
    """
    monkeypatch.setattr('sys.argv', [COMMAND, '--max-attempts=1', '--file=-'])
    mock_stdin_password_file_binary(monkeypatch, b'\x9b invalid-unicode\n')
    with pytest.raises(SystemExit) as exit_status:
        main()
    assert exit_status.value.code == 1


def test_main_run_no_args_invalid_answers(capsys, monkeypatch, mock_getpass) -> None:
    """
    Test running CLI entrypoint with no command line arguments, guessing
    the mocked password 100% wrong answers with mocked getpass input
    """
    max_attemps = 3
    monkeypatch.setattr('sys.argv', [COMMAND, f'--max-attempts={max_attemps}'])
    mock_stdin_password_file(monkeypatch, 'unexpected-password')
    script = PasswordTrainerScript()
    script.trainer.max_attempts = 2
    script.trainer.correct_password = 'something-different'
    with pytest.raises(SystemExit) as exit_status:
        script.run()
    assert exit_status.value.code == 0
    captured = capsys.readouterr()
    assert captured.err == ''
    assert len(captured.out.splitlines()) == 1
