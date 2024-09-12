#!/usr/bin/env python

import json

example_obj = {
    "DistinguishedName": "CN=First Name Last Name,OU=Standard,OU=Allusers,DC=corp,DC=example,DC=com",
    "Name": "First Name Last Name",
    "ObjectClass": "user",
    "ObjectGUID": "3e1038fb-14be-48f1-9d94-def71cd2104d",
    "l": "User City",
    "memberOf": [
        "CN=AP_AD_Group_1,OU=Groups,DC=corp,DC=example,DC=com",
        "CN=AP_AD_Group_2,OU=Groups,DC=corp,DC=example,DC=com",
        "CN=AP_AD_Group_3,OU=Groups,DC=corp,DC=example,DC=com"
    ],
    "userPrincipalName": "username@example.com"
}

count = 8000

print(json.dumps([example_obj for x in range(count)]))