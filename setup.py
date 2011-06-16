#!/usr/bin/env python

import os
import uploader.settings as settings

os.chdir("%/../" % settings.MEDIA_ROOT)

os.mkdir("db/")
os.system("python manage.py syncdb")
os.chdir(settings.MEDIA_URL)

try:
  os.mkdir("uploads/" % settings.MEDIA_ROOT)
except OSError:
  print("\n\n============= Everything is installed and up-to-date =============\n")
  print("\tRun server with commands: python manage.py runserver [[port]]\n")
