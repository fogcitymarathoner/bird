__author__ = 'marc'
import os
from fabric.api import run
from fabric.api import get
from fabric.api import local
from fabric.api import settings
from fabric.api import env

BASE_DIR = '.' # relative, absolute puts c: in front
SRC = BASE_DIR
APPS_DIR = os.path.join(BASE_DIR, 'apps')
ANGULAR_DIST = os.path.join(APPS_DIR, 'nodejs', 'dist')
EXCLUDES = '--exclude="local_settings.py" --exclude="*/tmp/*" --exclude=".git/*" ' \
           '--exclude="fabfile*" --exclude=".idea/"  --exclude="apps/nodejs/node_modules/"' \
            ' --exclude="apps/nodejs/.sass-cache" '
DEV_SRV = 'sfgeek.net'


def sync():
    """
    copy local changes in SRC to sfgeek.net:python_test_apps/bird using rsync
    :return:
    """
    cmd = 'find . | grep \.py$ | xargs chmod 644'
    local(cmd)
    cmd = 'rsync  -ahv --delete %s ' \
          ' %s %s:python_test_apps/bird'%(EXCLUDES, SRC, DEV_SRV)
    local(cmd)
