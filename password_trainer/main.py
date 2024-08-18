#
# Copyright (C) 2020-2024 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
import signal
import sys
from getpass import getpass
from typing import Any

from argparse import (
    ArgumentParser,
    FileType,
    Namespace,
    RawTextHelpFormatter
)

from .constants import (
    DEFAULT_ENCODING,
    DEFAULT_CORRECT_ANSWERS_REQUIRED,
    DEFAULT_MAXIMUM_ATTEMPTS_COUNT,
)
from .exceptions import PasswordTrainerError
from .trainer import PasswordTrainer

HINT_MESSAGE = 'New password to memorize: '
GUESS_PROMPT = 'Enter password to memorize: '
INITIAL_PASSWORD_PROMPT = 'Enter password to train for: '

DESCRIPTION = """Password trainer CLI

Train user's fingers to remeber specified password by repeatedly reading
the new password as input until requested number of correct passwords
have been given

The new password being trained on can be shown on the screen before
running the trainer. This option should not be used unless you are
in a secure place where your screen can not be viewed by anyone
"""


class PasswordTrainerScript:
    """
    Password trainer main CLI entrypoint script
    """
    parser: ArgumentParser
    trainer: PasswordTrainer

    def __init__(self) -> None:
        self.parser = self.initialize_parser()
        self.trainer = PasswordTrainer()
        signal.signal(signal.SIGINT, self.__SIGINT__)

    @staticmethod
    def initialize_parser() -> ArgumentParser:
        """
        Initialize ArgumentParser with required parameters for the
        password-trainer CLI
        """
        parser = ArgumentParser(
            description=DESCRIPTION,
            formatter_class=RawTextHelpFormatter,
        )
        parser.add_argument(
            '--debug',
            action='store_true',
            help='Show debug messages'
        )
        parser.add_argument(
            '-m', '--max-attempts',
            default=DEFAULT_MAXIMUM_ATTEMPTS_COUNT,
            type=int,
            help='Maximum number of attempts to write new password'
        )
        parser.add_argument(
            '-r', '--required',
            default=DEFAULT_CORRECT_ANSWERS_REQUIRED,
            type=int,
            help='Number of required correct answers before application exits'
        )
        parser.add_argument(
            '-f', '--file',
            type=FileType(mode='r', encoding=DEFAULT_ENCODING),
            help='New password to train against from text file or stdin'
        )
        parser.add_argument(
            '-s', '--show-password',
            action='store_true',
            help='Show new password to train with on screen (INSECURE)'
        )
        return parser

    def __SIGINT__(self, signum, frame):
        """
        Handle SIGINT signal to the script (Ctrl-C). Print message
        and exit with code 0
        """
        self.trainer.error('Interrupted')
        self.exit()

    def __read_password_input_file__(self, password_input_file: FileType) -> str:
        """
        Read password to train for from stdin or file
        """
        try:
            value = password_input_file.readline().rstrip()
            if isinstance(value, bytes):
                value = str(value, encoding=DEFAULT_ENCODING)
            return value
        except (OSError, UnicodeDecodeError) as error:
            raise PasswordTrainerError(
                f'Error reading password from file input: {error}'
            ) from error

    def configure_trainer(self, args: Namespace) -> None:
        """
        Configure password trainer parameters
        """
        if args.file:
            correct_password = self.__read_password_input_file__(args.file)
        else:
            correct_password = getpass(INITIAL_PASSWORD_PROMPT).strip()
        if not correct_password:
            raise PasswordTrainerError('No password to train against provided')

        self.trainer.configure(
            correct_password=correct_password,
            max_attempts=args.max_attempts,
            required=args.required,
        )

    def exit(self, code=0, *args: list[Any]) -> None:
        """
        Exit program with specified status code and optional error message
        """
        if args:
            self.trainer.error(*args)
        sys.exit(code)

    def parse_args(self) -> Namespace:
        """
        Parse arguments from command line
        """
        args = self.parser.parse_args()
        if args.debug:
            self.trainer.debug_enabled = True
        return args

    def show_results(self) -> None:
        """
        Print summary of the password trainer run results
        """
        self.trainer.message(
            f'Total {self.trainer.attempts} attempts, '
            f'{self.trainer.correct} answers ({self.trainer.percentage}%)'
        )

    def run(self) -> None:
        """
        Get user input to guess password and update stats
        """
        try:
            args = self.parse_args()
            self.configure_trainer(args)
            if args.show_password:
                self.trainer.message(f'{HINT_MESSAGE}{self.trainer.correct_password}')
            while True:
                try:
                    self.trainer.match(getpass(GUESS_PROMPT).strip())
                except StopIteration:
                    break
            self.show_results()
            self.exit()
        except PasswordTrainerError as error:
            self.exit(1, error)


def main():
    """
    Main entrypoint for the password-trainer CLI
    """
    PasswordTrainerScript().run()
