#!/usr/bin/env python

import os
import uploader.settings as settings

try:
  os.mkdir("%s/uploads/" % settings.MEDIA_ROOT)
except OSError:
  print("\n\n============= Everything is installed and up-to-date =============\n")
  print("\tRun server with commands: python manage.py runserver [[port]]\n")
