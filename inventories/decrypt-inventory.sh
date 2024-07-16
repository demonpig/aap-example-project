#!/bin/sh

TEMP_FILE="$RANDOM"

ansible-vault view --vault-password-file=${FOOBAR:-""} "$(dirname $0)/${ENCRYPTED_FILENAME:-encrypted-inventory.yml}" > $TEMP_FILE

ansible-inventory --list --export -i $TEMP_FILE

rm -f $TEMP_FILE
