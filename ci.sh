#!/bin/bash
set -e


# ----------------------------
# Unit Tests
# ----------------------------
echo -e "\e[32mStarting Unit Tests\e[39m"
cd tests
PYTHONPATH=../raytracer python -m unittest discover .
cd -

# ----------------------------
# Check types
# ----------------------------
echo -e "\e[32mStarting Type Checks\e[39m"
mypy raytracer

# ----------------------------
# Check code quality threshold
# ----------------------------
echo -e "\e[32mStarting Linting\e[39m"
# n.b. the threshold here was set to the code quality on the first commit of
# this code (6.11).  Going forward, the number has to keep going up, and every
# time it passes another 0.1, I move this parameter
pylint raytracer --fail-under 8

echo -e "\e[32mCompleted successfully\e[39m"
