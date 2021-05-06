# All Redis Graph client tests

To keep code working properly and looking good it's critical to cover
all functionality with unit and functional tests and use automated code style
checks.

Unit tests are tests that focus is to test line by line all code of library
where any of external dependencies need in runtime (like redisgraph) are mocked

Functional tests on other hand act like black box testing, where we make sure
that client when used with real redisgraph is working properly

Code style checks are analyzing code style, to make sure code looks like
written by one person.

Combination of these 3 approaches will ensure high quality of the code.


To launch test please use: ```tox -e func```

## Requirements to run tests locally

Redisgraph is using tox, highly popular tool that aims to automate and
standardize testing in Python.

For more details https://tox.readthedocs.io/en/latest/

To install it locally run ```pip install tox```


## Running tests locally

```bash

# To run all tests
tox

# To run py3 tests
tox -e py3

# To run code style checks
tox -e pep8

# To run unittests with coverage
tox -e cover

# To run functional test use
# Make sure that redis is running locally on standard port 6379
tox -e func

```
