#!/usr/bin/env python

import json

def _generate_inventory():
    data = {
        "_meta": {
            "hostvars": {
                "desktop-hitmebabyonemoretime": {
                    "ansible_host": "DESKTOP-HITMEBABYONEMORETIME.example.org",
                    "computer_guid": {
                        "__ansible_unsafe": "7c1ba40a-5885-40c0-8d24-c1c7b3ab990c"
                    },
                    "computer_lastseen_at": "2010-01-01T00:00:00.000000+0000",
                    "computer_membership": [],
                    "computer_name": {
                        "__ansible_unsafe": "DESKTOP-HITMEBABYONEMORETIME"
                    },
                    "computer_sid": {
                        "__ansible_unsafe": "S-2-3-4-*****"
                    },
                    "microsoft_ad_distinguished_name": "CN=DESKTOP-HITMEBABYONEMORETIME,OU=Computers,OU=Eng,DC=example,DC=org",
                    "os_name": {
                        "__ansible_unsafe": "Windows 10 Enterprise"
                    },
                    "os_version": {
                        "__ansible_unsafe": "10.0 (17134)"
                    }
                }
            }
        },
        "all": {
            "children": [
                "ungrouped",
                "windows"
            ]
        },
        "windows": {
            "hosts": [
                {
                    "__ansible_unsafe": "desktop-hitmebabyonemoretime"
                }
            ]
        }
    }


    return json.dumps(data)

if __name__ == '__main__':
    print(_generate_inventory())
