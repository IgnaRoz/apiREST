[![Tests](https://github.com/IgnaRoz/apiREST/actions/workflows/tests.yml/badge.svg)](https://github.com/IgnaRoz/apiREST/actions/workflows/tests.yml)
[![Tests integracion](https://github.com/IgnaRoz/apiREST/actions/workflows/testsIntegracion.yml/badge.svg)](https://github.com/IgnaRoz/apiREST/actions/workflows/testsIntegracion.yml)
[![Linters](https://github.com/IgnaRoz/apiREST/actions/workflows/linters.yml/badge.svg)](https://github.com/IgnaRoz/apiREST/actions/workflows/linters.yml)
[![Type checking](https://github.com/IgnaRoz/apiREST/actions/workflows/typechecking.yml/badge.svg)](https://github.com/IgnaRoz/apiREST/actions/workflows/typechecking.yml)

# Token Service for ADI 2024-2025

## Installation

To locally install the package, just run

```
pip install .
```

Or, if you want to modify it during your development,

```
pip install -e .
```

## Execution

To run the server, just install the package and run

```
token_service
```

## Running tests and linters locally

If you want to run the tests and/or linters, you need to install the dependencies for them:

- To install test dependencies: `pip install .[tests]`
- To install linters dependencies: `pip install .[linters]`

All the tests runners and linters are configured in the `pyproject.toml`.

## Continuous integration

This repository is already configured to run the following workflows:

- Ruff: checks the format, code style and docs style of the source code.
- Pylint: same as Ruff, but it evaluates the code. If the code is rated under a given threshold, it fails.
- MyPy: checks the types definitions and the usages, showing possible errors.
- Unit tests: uses `pytest` to run unit tests. The code coverage is quite low. Fixing the tests, checking the
    test coverage and improving it will make a difference.

If you create your repository from this template, you will get all those CI for free.
