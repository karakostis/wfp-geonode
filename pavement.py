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

from paver.easy import sh, task

@task
def run_tests(options):
    """
    Run WFP GeoNode's Unit Test Suite
    """
    sh("python manage.py test wfp.trainings.tests.tests wfp.wfpdocs.tests.tests --settings=wfp.settings.testing --traceback")
    sh('flake8 wfp --max-line-length=120')
