#
# Copyright (C) 2020-2024 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Helper classes for unit tests
"""
from io import BytesIO, StringIO

MAIN_GETPASS_METHOD = 'password_trainer.main.getpass'


class MockGetPass:
    """
    Mock returning specified password value
    """
    def __init__(self, value: str = 'password') -> None:
        self.value = value

    def __call__(self, *args, **kwargs) -> str:
        """
        Return static value
        """
        return f'{self.value}\n'


def add_getpass_mock(monkeypatch, value: str = 'password') -> None:
    """
    Set getpass() value returned to specified value
    """
    monkeypatch.setattr(MAIN_GETPASS_METHOD, MockGetPass(value))


def mock_stdin_password_file(monkeypatch, value: str = 'password') -> None:
    """
    Mock reading specified input password from stdin string
    """
    monkeypatch.setattr('sys.stdin', StringIO(value))


def mock_stdin_password_file_binary(monkeypatch, value: bytes) -> None:
    """
    Mock reading specified input password from stdin as bytes
    """
    monkeypatch.setattr('sys.stdin', BytesIO(value))
