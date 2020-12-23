#!/bin/bash

cd tests
python -m unittest discover .
cd -

mypy raytracer
