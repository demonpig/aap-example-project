#!/bin/sh

INV_FILENAME="$(dirname $0)/${CUSTOM_VAULT_INVENTORY}"

test -f "${INV_FILENAME}" || { echo "Inventory not found"; exit 2; }
test -f "${CUSTOM_VAULT_PASSWORD_FILE}" || { echo "ansible-vault password file not found"; exit 3; }

ansible-inventory --list --export --vault-password-file ${CUSTOM_VAULT_PASSWORD_FILE} -i "${INV_FILENAME}"
