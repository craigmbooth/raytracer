#!/bin/bash
set -e

cd tests
python -m unittest discover .
cd -

mypy raytracer
