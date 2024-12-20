#!/usr/bin/env python
# This is a simplified example of what a dynamic inventory script might look like.
import json

print(json.dumps({
    "all": {
        "hosts": [
            "server1.example.com",
            "server2.example.com"
        ]
    }
}))