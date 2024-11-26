#!/usr/bin/python3

import base64

message = "my_username:my_password"
encoded_message = base64.b64encode(message.encode()).decode()
print(encoded_message)