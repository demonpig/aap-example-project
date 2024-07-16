#!/bin/sh

ansible-vault view --vault-password-file=${FOOBAR:-""} "$(dirname $0)/encrypted-inventory.yml"
