#!/usr/bin/env python
#########################################################################
#
# Copyright (C) 2012-2015 Paolo Corti, pcorti@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

from __future__ import absolute_import

import subprocess
import datetime
import os

NAME = 'wfp-geonode'
VERSION = __version__ = (2, 4, 6, 'final', 0)
__author__ = 'WFP development team, Paolo Corti (pcorti@gmail.com)'


def get_version():  # pragma: no cover
    """Derives a PEP386-compliant version number from VERSION."""
    assert len(VERSION) == 5
    assert VERSION[3] in ('alpha', 'beta', 'rc', 'final')

    parts = 2 if VERSION[2] == 0 else 3
    main = '.'.join(str(x) for x in VERSION[:parts])

    sub = ''
    if VERSION[3] == 'alpha' and VERSION[4] == 0:
        git_changeset = get_git_changeset()
        if git_changeset:
            sub = '.dev%s' % git_changeset

    elif VERSION[3] != 'final':
        mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'c'}
        sub = mapping[VERSION[3]] + str(VERSION[4])
    elif VERSION[3] == 'final':
        if VERSION[4] > 0:
            sub += '-%s' % VERSION[4]

    return main + sub


def get_git_changeset():  # pragma: no cover
    """Returns a numeric identifier of the latest git changeset.

    The result is the UTC timestamp of the changeset in YYYYMMDDHHMMSS format.
    This value isn't guaranteed to be unique, but collisions are very unlikely,
    so it's sufficient for generating the development version numbers.
    """
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    git_log = subprocess.Popen('git log --pretty=format:%ct --quiet -1 HEAD',
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               shell=True, cwd=repo_dir, universal_newlines=True)
    timestamp = git_log.communicate()[0]
    try:
        timestamp = datetime.datetime.utcfromtimestamp(int(timestamp))
    except ValueError:
        return None
    return timestamp.strftime('%Y%m%d%H%M%S')
