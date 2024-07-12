#!/usr/bin/bash

PYTHON_BIN="python3"

command -v $PYTHON_BIN > /dev/null || exit 100

$PYTHON_BIN "$(dirname $0)/dynamic_inventory.py"
