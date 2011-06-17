#!/usr/bin/env python

import os
import uploader.settings as settings

os.chdir("%s/../" % settings.MEDIA_ROOT)

try:
  os.mkdir("db/")
except OSError:
  pass

os.system("python manage.py syncdb")
os.chdir(settings.MEDIA_URL)

try:
  os.mkdir("uploads/")
except OSError:
  print("\n\n============= Everything is installed and up-to-date =============\n")
  print("\tRun server with commands: python manage.py runserver [[port]]\n")
