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

import random
from datetime import date

from django_dynamic_fixture import G

from wfp.trainings.models import Training
from geonode.layers.models import Layer


def get_random_date():
    """ Generate a random date """
    start_date = date.today().replace(day=1, month=1).toordinal()
    end_date = date.today().toordinal()
    return date.fromordinal(random.randint(start_date, end_date))


def training_factory(**kwargs):
    """ Factory for a random training """
    training_number = random.randint(0, 1000)
    title = kwargs.pop('title', None)
    if not title:
        title = 'Training N. %s' % training_number
    abstract = 'Abstract for training N. %s' % training_number
    publication_date = get_random_date()
    training = G(Training, title=title, publication_date=publication_date,
                 abstract=abstract)

    # append some (0 to 5) layers
    id_list = list(xrange(Layer.objects.all().count()))
    random.shuffle(id_list)
    num_layers_to_append = random.randint(0, 5)
    for i in range(0, num_layers_to_append):
        layer = Layer.objects.all()[id_list[i]]
        training.layers.add(layer)

    # append some (0 to 5) keywords
    keywords = ['gis', 'gdal', 'geoserver', 'geonode', 'qgis', 'postgis',
                'osgeo', 'pyqgis', 'django']
    random.shuffle(keywords)
    num_keywords_to_append = random.randint(0, 5)
    for i in range(0, num_keywords_to_append):
        training.keywords.add(keywords[i])

    return training
