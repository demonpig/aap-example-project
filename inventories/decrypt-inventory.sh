#!/bin/sh

ls $CUSTOM_VAULT_INVENTORY > /dev/null || { echo "Inventory not found" ; exit 2; }

ansible-inventory --list --export --vault-password-file ${CUSTOM_VAULT_PASSWORD_FILE:-""} -i "$(dirname $0)/$CUSTOM_VAULT_INVENTORY"
