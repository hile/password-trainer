#
# Copyright (C) 2020-2024 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for password_trainer.utils module
"""
import os

from password_trainer.constants import ENV_PASSWORD_TRAINER_PREFIX
from password_trainer.utils import (
    get_env_boolean_flag,
    var_is_false,
    var_is_true,
)

TEST_BOOLEAN_VAR = 'demo_boolean'
TEST_BOOLEAN_ENV_VAR: str = f'{ENV_PASSWORD_TRAINER_PREFIX}{TEST_BOOLEAN_VAR}'.upper()


def test_var_is_true_lowercase(true_string_lowercase) -> None:
    """
    Test var_is_true() with valid lowercase truish strings
    """
    assert var_is_true(true_string_lowercase)


def test_var_is_true_uppercase(true_string_uppercase) -> None:
    """
    Test var_is_true() with valid uppercase truish strings
    """
    assert var_is_true(true_string_uppercase)


def test_var_is_false_lwercase(false_string_lowercase) -> None:
    """
    Test var_is_false() with valid lowercase falseish strings
    """
    assert var_is_false(false_string_lowercase)


def test_var_is_false_uppercase(false_string_uppercase) -> None:
    """
    Test var_is_false() with valid uppercase falseish strings
    """
    assert var_is_false(false_string_uppercase)


def test_get_env_boolean_flag_env_undefined_default(monkeypatch) -> None:
    """
    Test parsing boolean environment variable when var is not defined in environment
    """
    if TEST_BOOLEAN_ENV_VAR in os.environ:
        monkeypatch.delenv(TEST_BOOLEAN_ENV_VAR)
    assert get_env_boolean_flag(TEST_BOOLEAN_VAR) is False


def test_get_env_boolean_flag_env_undefined_specified_default(monkeypatch) -> None:
    """
    Test parsing boolean environment variable when var is not defined in environment
    """
    if TEST_BOOLEAN_ENV_VAR in os.environ:
        monkeypatch.delenv(TEST_BOOLEAN_ENV_VAR)
    assert get_env_boolean_flag(TEST_BOOLEAN_VAR, default=True) is True


def test_get_env_boolean_flag_false_lowercase(monkeypatch, false_string_lowercase) -> None:
    """
    Test parsing boolean environment variable falseish values
    """
    monkeypatch.setenv(TEST_BOOLEAN_ENV_VAR, false_string_lowercase)
    assert get_env_boolean_flag(TEST_BOOLEAN_VAR) is False


def test_get_env_boolean_flag_true_lowercase(monkeypatch, true_string_lowercase) -> None:
    """
    Test parsing boolean environment variable truish values
    """
    monkeypatch.setenv(TEST_BOOLEAN_ENV_VAR, true_string_lowercase)
    assert get_env_boolean_flag(TEST_BOOLEAN_VAR) is True
