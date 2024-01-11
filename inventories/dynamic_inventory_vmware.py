#!/usr/bin/env python

# this is just a template

import json

def _generate_inventory():

    hostvars = {}
    hostvars['vmware_host1.local'] = {
        "ansible_connection": "winrm",
        "ansible_host": "localhost",
        "ansible_host_ip": "127.0.0.1",
        "ansible_port": 5985,
        "availability_zone": None,
        "computer_name": "localhost",
        "creation_time": "2000-01-01T00:00:00.6666452+00:00",
        "data_disks": [],
        "default_inventory_hostname": "localhost",
        "id": "/subscriptions/80842efe-e9fd-4ad3-ad2e-9f5aca54bcd4/resourceGroups/TEST-localhost/providers/Microsoft.Compute/virtualMachines/localhost",
        "image": {
            "id": "/subscriptions/c32bd846-23ea-4b5d-96c6-c5a588a4f127/resourceGroups/RT-US-PRD-ARG-Operations/providers/Microsoft.Compute/galleries/TEST_GALLERY/images/TEST_WINDOWS_2019_SOE"
        },
        "location": "australiaeast",
        "mac_address": [
            "00-11-48-11-FC-0F"
        ],
        "name": "localhost",
        "network_interface": [
            "localhost-nic01"
        ],
        "network_interface_id": [
            "/subscriptions/80842efe-e9fd-4ad3-ad2e-9f5aca54bcd4/resourceGroups/TEST-localhost/providers/Microsoft.Network/networkInterfaces/localhost-nic01"
        ],
        "os_disk": {
            "id": "/subscriptions/80842efe-e9fd-4ad3-ad2e-9f5aca54bcd4/resourceGroups/TEST-localhost/providers/Microsoft.Compute/disks/localhost-OS-disk",
            "name": "localhost-OS-disk",
            "operating_system_type": "windows"
        },
        "os_profile": {
            "system": "windows"
        },
        "os_type": "windows",
        "plan": None,
        "powerstate": "running",
        "private_ip": "127.0.0.1",
        "private_ipv4_addresses": [
            "127.0.0.1"
        ],
        "provisioning_state": "Succeeded",
        "public_dns_hostnames": [],
        "public_ip": None,
        "public_ip_id": None,
        "public_ip_name": None,
        "public_ipv4_addresses": [],
        "resource_group": "TEST-localhost",
        "resource_type": "Microsoft.Compute/virtualMachines",
        "security_group": [],
        "security_group_id": [],
        "tags": {
            "CompanyName": "EXAMPLE",
            "CostCode": "91007200",
            "CreatedDate": "1/01/2000 00:00:00 PM",
            "Creator": "Admin",
            "Environment": "Non Production",
            "FinanceCode": "A111"
        },
        "type": "Microsoft.Compute/virtualMachines",
        "virtual_machine_size": "Standard_B2ms",
        "vmid": "50b66256-d378-411f-bf4c-9d5c6276facf",
        "vmss": {}
    }

    ungrouped = list(hostvars.keys())

    data = {
        '_meta': {
            'hostvars': hostvars
        },
        'all': {
            'children': ['ungrouped']
        },
        'ungrouped': {
            'hosts': ungrouped
        }
    }

    return json.dumps(data)

if __name__ == '__main__':
    print(_generate_inventory())
