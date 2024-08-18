#
# Copyright (C) 2020-2024 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for password_trainer.trainer module
"""
import pytest

from password_trainer.constants import (
    DEFAULT_CORRECT_ANSWERS_REQUIRED,
    DEFAULT_MAXIMUM_ATTEMPTS_COUNT,
)
from password_trainer.exceptions import PasswordTrainerError
from password_trainer.trainer import PasswordTrainer

from .constants import MESSAGE, DEBUG_MESSAGE


def test_password_trainer_uninitialzied_object_properties() -> None:
    """
    Ensure password trainer correct_password att
    """
    trainer = PasswordTrainer()
    assert trainer.attempts == 0
    assert trainer.correct == 0
    assert trainer.max_attempts == DEFAULT_MAXIMUM_ATTEMPTS_COUNT
    assert trainer.required == DEFAULT_CORRECT_ANSWERS_REQUIRED
    assert trainer.correct_password is None


def test_password_trainer_debug_disabled(capsys, env_debug_disabled) -> None:
    """
    Test PasswordTrainerScript object debug method when diabled
    """
    trainer = PasswordTrainer()
    trainer.debug(MESSAGE)
    trainer.message(MESSAGE)
    captured = capsys.readouterr()
    assert captured.err == ''
    assert captured.out.splitlines() == [MESSAGE]


def test_password_trainer_debug_enabled(capsys, env_debug_enabled) -> None:
    """
    Test PasswordTrainerScript object debug method when enabled
    """
    trainer = PasswordTrainer()
    trainer.debug(MESSAGE)
    trainer.message(MESSAGE)
    captured = capsys.readouterr()
    assert captured.err.splitlines() == [DEBUG_MESSAGE]
    assert captured.out.splitlines() == [MESSAGE]


def test_password_trainer_percentage_no_data() -> None:
    """
    Ensure password trainer return 0 percentage value when there
    are no training attempts done
    """
    assert PasswordTrainer().percentage == 0


def test_password_trainer_percentage_0() -> None:
    """
    Ensure password trainer return 0 percentage value when there
    are no training attempts done
    """
    trainer = PasswordTrainer()
    trainer.correct = 0
    trainer.attempts = 11
    assert trainer.percentage == 0


def test_password_trainer_percentage_100() -> None:
    """
    Ensure password trainer return 0 percentage value when there
    are no training attempts done
    """
    trainer = PasswordTrainer()
    trainer.correct = 11
    trainer.attempts = 11
    assert trainer.percentage == 100


def test_password_trainer_match_unconfigured() -> None:
    """
    Ensure password trainer return 0 percentage value when password
    trainer is not yet initialized with trained password
    """
    with pytest.raises(PasswordTrainerError):
        PasswordTrainer().match('test')
