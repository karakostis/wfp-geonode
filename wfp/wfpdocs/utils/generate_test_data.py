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

from django.core.files import File
from random import randint

from geonode.documents.models import Document
from geonode.people.models import Profile
from geonode.base.models import TopicCategory


def create_document(number):
    print 'Generating image %s' % number
    admin = Profile.objects.filter(username='admin')[0]

    file_list = (
                    '1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg', '7.jpg',
                    '8.jpg', '9.png', '10.jpg', '11.jpg',)
    random_index = randint(0, 10)
    file_uri = '/home/capooti/Desktop/maps/%s' % file_list[random_index]
    title = 'Document N. %s' % number
    img_filename = '%s_img.jpg' % number

    doc = Document(title=title, owner=admin)
    doc.save()
    with open(file_uri, 'r') as f:
        img_file = File(f)
        doc.doc_file.save(img_filename, img_file, True)

    base = doc.get_self_resource()
    random_index = randint(0, 18)
    tc = TopicCategory.objects.all()[random_index]
    base.category = tc
    base.save()


for i in range(790, 5000):
    create_document(i)
