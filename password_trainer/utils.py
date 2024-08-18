#
# Copyright (C) 2020-2024 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
import os

from .constants import (
    ENV_PASSWORD_TRAINER_PREFIX,
    ENV_FALSE_STRINGS,
    ENV_TRUE_STRINGS,
)


def get_env_boolean_flag(var: str, default: bool = False) -> bool:
    """
    Look up specified variable from environment variables prefixed by common prefix

    The variable value is

    Returns True if environment variable is defined and is set to 1
    """
    env_var = f'{ENV_PASSWORD_TRAINER_PREFIX}{var}'.upper()
    value = os.environ.get(env_var, None)
    if var_is_true(value):
        return True
    if var_is_false(value):
        return False
    return default


def var_is_false(var: str | None) -> bool:
    """
    Match specified string value to falseish values

    Return True if variable is not defined or has one of specified falseish strings,
    ignoring case of the string
    """
    if not var:
        return False
    return var.lower() in ENV_FALSE_STRINGS


def var_is_true(var: str | None) -> bool:
    """
    Match specified string value to truish values

    Return True if variable is defined and has one of specified truish strings,
    ignoring case of the string
    """
    if not var:
        return False
    return var.lower() in ENV_TRUE_STRINGS
