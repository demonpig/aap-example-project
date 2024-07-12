#!/usr/bin/bash

PYTHON_BIN="python3"

command -v $PYTHON_BIN || exit 100

$PYTHON_BIN dynamic_inventory.py
