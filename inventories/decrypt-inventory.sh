#!/bin/sh

ansible-vault view --vault-password-file=${FOOBAR:-""} encrypted-inventory.yml