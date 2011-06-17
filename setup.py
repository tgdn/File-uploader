#!/usr/bin/env python

import os
import uploader.settings as settings

os.chdir("%s/../" % settings.MEDIA_ROOT)

try:
  os.mkdir("db/")
except OSError:
  pass

os.system("python manage.py syncdb")

try:
  os.mkdir("media/uploads")
except OSError:
  pass

print("\n\n============= Everything is installed and up-to-date =============\n")
print("\tRun server with commands: python manage.py runserver [[port]]\n")
