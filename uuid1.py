#!/usr/bin/env python
import uuid

import pyperclip

uuid_now = str(uuid.uuid1())

pyperclip.copy(uuid_now)
print("CLIPPED:", uuid_now)
