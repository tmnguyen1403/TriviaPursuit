#!/bin/bash
# Using this scrip to setup PYTHONPATH for the game
PYTHONPATH="${PYTHONPATH}:$(dirname "$(pwd)")"
PYTHONPATH="${PYTHONPATH}:$(pwd))"

export PYTHONPATH