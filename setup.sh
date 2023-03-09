#!/bin/bash

# Install PipEnv
python3 -m pip install --user poetry
# Install Dependencies
python3 -m poetry install
# Install Pre-Commit
python3 -m poetry run pre-commit install
# Incase Lock file is already present, sync it curr dependecies
python3 -m poetry lock --no-update
# Setup CI Test Requirements
python3 -m poetry export --with dev --with test --without-hashes -f requirements.txt --output requirements.txt
# docker
docker-compose up -d --build --remove-orphans
# Enter Shell
python3 -m poetry shell
