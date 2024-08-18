![Unit Tests](https://github.com/hile/password-trainer/actions/workflows/unittest.yml/badge.svg)
![Style Checks](https://github.com/hile/password-trainer/actions/workflows/lint.yml/badge.svg)

# Password trainer script

This module contains a litle script to teach user a new random password by
repeatedly typing it. The module is written in pure python and contains no
external dependencies except for poetry build system and modules used for
testing the code. The code should be very simple to review.

The idea is to use this tool with a password generator and some kind of
password manager to ensure user does not *remember* the password but can
write it without looking. It's not intended to replace password managers,
it's intended to memorize password for primary logins and for the
password manager master keys.

General procedure for me while using the tool:

- generate new password for a system and store it to password manager
- run this password trainer a couple of times with the password from the
  password manager, training my fingers to write the password mechanically
- repeat it for a couple of days until sucecss rate is 100% and then
  change the actual password for the system

## Using the password trainer

The tool is installed as command line *password-trainer*. The tool reads
password from stdin or file (for reading from password managers) or
interactively. User is then requested to write the new password on screen
until configured number of correct passwords has been entered. The tool
shows a summary of success rate when it quits.

Parameters for the training phase can be specified as command line arguments.
See *password-trainer --help* for more details.

## Example commands

bash```
echo foo | password-trainer --required=1 --password-input-file=-
````

## Installing

This module has minimal dependencies (PyYAML) and should install with *pip*
on any recent python version.

The module has been tested with python 3.10 to 3.12.

## Running unit tests and linters

All tests are run with *tox*.

Run unit tests and linters:

```bash
make
```

Run unit tests:

```bash
make test
```

Run linters:

```bash
make lint
```
