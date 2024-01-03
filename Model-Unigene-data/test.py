#!/usr/bin/env python3

import requests
import simplejs

r = requests.get('https://httpbin.org/basic-auth/user/pass', auth=('user', 'pass'))
print(r.status_code)
