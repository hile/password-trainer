#
# Copyright (C) 2020-2024 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit test configuration for password_trainer module
"""
import os
from collections.abc import Generator

import pytest

from password_trainer.constants import (
    ENV_PASSWORD_TRAINER_PREFIX,
    ENV_TRUE_STRINGS,
    ENV_FALSE_STRINGS,
)
from .helpers import add_getpass_mock

ENV_DEBUG_FLAG = f'{ENV_PASSWORD_TRAINER_PREFIX}DEBUG'


@pytest.fixture(params=ENV_FALSE_STRINGS)
def false_string_lowercase(request) -> Generator[str]:
    """
    Unit test fixture to return known false string values in lowercase
    """
    yield (request.param.lower())


@pytest.fixture(params=ENV_FALSE_STRINGS)
def false_string_uppercase(request) -> Generator[str]:
    """
    Unit test fixture to return known false string values in uppercase
    """
    yield (request.param.upper())


@pytest.fixture(params=ENV_TRUE_STRINGS)
def true_string_lowercase(request) -> Generator[str]:
    """
    Unit test fixture to return known true string values in lowercase
    """
    yield (request.param.lower())


@pytest.fixture(params=ENV_TRUE_STRINGS)
def true_string_uppercase(request) -> Generator[str]:
    """
    Unit test fixture to return known true string values in uppercase
    """
    yield (request.param.upper())


@pytest.fixture
def env_debug_disabled(monkeypatch) -> None:
    """
    Disable debug flag in environment variables
    """
    if ENV_DEBUG_FLAG in os.environ:
        monkeypatch.delenv(ENV_DEBUG_FLAG)


@pytest.fixture
def env_debug_enabled(monkeypatch) -> None:
    """
    Enabe debug flag in environment variables
    """
    monkeypatch.setenv(ENV_DEBUG_FLAG, ENV_TRUE_STRINGS[0])


@pytest.fixture
def mock_getpass(monkeypatch) -> None:
    """
    Return known value for getpass
    """
    add_getpass_mock(monkeypatch, 'password')
