#
# Copyright (C) 2020-2024 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
import sys
from typing import Any

from .constants import (
    DEFAULT_CORRECT_ANSWERS_REQUIRED,
    DEFAULT_MAXIMUM_ATTEMPTS_COUNT,
)
from .exceptions import PasswordTrainerError
from .utils import get_env_boolean_flag

PASSWORD_GUESS_NO_MATCH = 'Incorrect password'


class PasswordTrainer:
    """
    Password trainer utility
    """
    attempts: int
    correct: int
    required: int
    max_attempts: int
    correct_password: str | None

    debug_enabled: bool

    def __init__(self,
                 correct_password: str | None = None,
                 max_attempts: int = DEFAULT_MAXIMUM_ATTEMPTS_COUNT,
                 required: int = DEFAULT_CORRECT_ANSWERS_REQUIRED) -> None:
        self.debug_enabled = get_env_boolean_flag('DEBUG')
        self.correct_password = None
        self.configure(
            correct_password=correct_password,
            max_attempts=max_attempts,
            required=required
        )

    def __format_message__(self, *args: list[Any]) -> str:
        """
        Format specified as a string separated by single space
        """
        return ' '.join(str(arg) for arg in args)

    @property
    def percentage(self) -> int:
        """
        Return percentage of correct guesses
        """
        if not self.attempts:
            return 0
        return int(self.correct / self.attempts * 100)

    def configure(self,
                  correct_password: str | None = None,
                  max_attempts: int = DEFAULT_MAXIMUM_ATTEMPTS_COUNT,
                  required: int = DEFAULT_CORRECT_ANSWERS_REQUIRED) -> None:
        """
        Configure password trainer
        """
        self.attempts = 0
        self.correct = 0
        self.max_attempts = max_attempts
        self.required = required
        if correct_password is not None:
            self.correct_password = correct_password

    def debug(self, *args: list[Any]) -> None:
        """
        Write debug message to stderr if self.__debug_enabled__ true
        """
        if not self.debug_enabled:
            return
        self.error(f'DEBUG {self.__format_message__(*args)}')

    def error(self, *args: list[Any]) -> None:
        """
        Write specified message to sys.stderr and flush the stream
        """
        sys.stderr.write(f'{self.__format_message__(*args)}\n')
        sys.stderr.flush()

    def message(self, *args: list[Any]) -> None:
        """
        Write specified message to sys.stdout and flush the stream
        """
        sys.stdout.write(f'{self.__format_message__(*args)}\n')
        sys.stdout.flush()

    def match(self, password_guess: str) -> bool:
        """
        Match specifed password to correct password, increasing counters and
        optionally show error messages

        StopIteration is raised when number of required attemps is reached
        """
        if not self.correct_password:
            raise PasswordTrainerError('Password trainer is not yet configured')

        correct: bool = True
        self.attempts += 1
        if password_guess == self.correct_password:
            self.correct += 1
        else:
            self.message(PASSWORD_GUESS_NO_MATCH)
            correct = False

        if self.correct >= self.required or self.attempts >= self.max_attempts:
            raise StopIteration

        return correct
