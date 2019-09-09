#!/usr/bin/env python
import os.path
import sys

DIRNAME = os.path.dirname(__file__)
# trick to get the two-levels up directory, which for the "simple" project should be the satchmo dir
_parent = lambda x: os.path.normpath(os.path.join(x, '..'))

SATCHMO_DIRNAME = _parent(_parent(DIRNAME))
SATCHMO_APPS = os.path.join(SATCHMO_DIRNAME, 'apps')
PROJECTS = os.path.join(SATCHMO_DIRNAME, 'projects')

if not SATCHMO_APPS in sys.path:
    sys.path.append(SATCHMO_APPS)

if not DIRNAME in sys.path:
    sys.path.append(DIRNAME)

if not PROJECTS in sys.path:
    sys.path.append(PROJECTS)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "skeleton.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
