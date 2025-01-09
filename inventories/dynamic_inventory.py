#!/usr/bin/env python

import json

count = 10

def _generate_inventory():

    ungrouped = ["host_{}.local".format(i) for i in range(count)]

    hostvars = {}
    for i in range(count):
        name = "host_{}.local".format(i)
        hostvars[name] = {'ansible_host': '', 'ansible_connection': ''}
        hostvars[name]['ansible_host'] = '127.0.0.1'
        hostvars[name]['ansible_connection'] = 'local'

    data = {
        '_meta': {
            'hostvars': hostvars
        },
        'all': {
            'children': ['ungrouped']
        },
        'ungrouped': {
            'hosts': ungrouped
        },
        "group_1": {
            'hosts': ungrouped[0:10]
        }
    }

    return json.dumps(data)

if __name__ == '__main__':
    print(_generate_inventory())
