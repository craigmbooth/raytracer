#!/bin/bash
set -e

# ----------------------------
# Unit Tests
# ----------------------------
cd tests
python -m unittest discover .
cd -

# ----------------------------
# Check types
# ----------------------------
mypy raytracer

# ----------------------------
# Check code quality threshold
# ----------------------------
pylint raytracer --fail-under 6.2

# Note that pylint doesn't really dispay an error, it just does it with an error code.  Need to clean up printing here, and show error messages
