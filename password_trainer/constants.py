#
# Copyright (C) 2020-2024 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Constants for the password trainer application
"""

# Default encoding for password strings
DEFAULT_ENCODING = 'utf-8'

# Default number of answers required to be correct
DEFAULT_CORRECT_ANSWERS_REQUIRED = 5

# Default value for maximum number of guesses
DEFAULT_MAXIMUM_ATTEMPTS_COUNT = 10

# Prefix for environment variables for the application
ENV_PASSWORD_TRAINER_PREFIX = 'PASSWORD_TRAINER_'

# Environment variables considered as True boolean value, ignoring case
ENV_TRUE_STRINGS = (
    '1',
    'yes',
    'true',
)

# Environment variables considered as True boolean value, ignoring case
ENV_FALSE_STRINGS = (
    '0',
    'no',
    'false',
)
