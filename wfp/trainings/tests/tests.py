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

import StringIO

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from tastypie.test import ResourceTestCase

from geonode.base.populate_test_data import create_models

from wfp.trainings.models import Training
from wfp.trainings.tests.fixtures import training_factory, get_random_date


class TrainingTest(TestCase):

    def setUp(self):
        create_models('layer')

    def test_training_creation(self):
        """ Tests the creation of a training with some layers """

        title = 'Test Training with Layers'
        training = training_factory(title=title)
        self.assertEquals(Training.objects.get(pk=training.id).title, title)

    def test_training_details(self):
        """ Tests accessing the details view of a training """

        training = training_factory()

        c = Client()
        response = c.get(reverse('training_detail', args=(str(training.id),)))
        self.assertEquals(response.status_code, 200)

    def test_training_upload(self):
        """ Tests uploading a new training """

        logo_file = StringIO.StringIO(
            'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00'
            '\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;')
        logo = SimpleUploadedFile(
            'logo_test_file.gif', logo_file.read(), 'image/gif')
        manual_file = StringIO.StringIO(
            'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00'
            '\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;')
        manual = SimpleUploadedFile(
            'logo_test_file.gif', manual_file.read(), 'image/gif')

        c = Client()
        c.login(username='admin', password='admin')
        c.post(
            reverse('training_upload'),
            data={
                    'title': 'Uploaded Training',
                    'abstract': 'Abstract for uploaded training',
                    'publication_date': get_random_date(),
                    'logo': logo,
                    'manual': manual,
                 },
            follow=True)

        self.assertEquals(Training.objects.all().count(), 1)

        training = Training.objects.all()[0]
        c = Client()
        response = c.get(reverse('training_detail', args=(str(training.id),)))
        self.assertEquals(response.status_code, 200)


class TrainingApiTest(ResourceTestCase):

    def setUp(self):
        super(TrainingApiTest, self).setUp()

        self.username = 'admin'
        self.password = 'admin'
        self.list_url = reverse(
            'api_dispatch_list',
            kwargs={
                'api_name': 'v2.4',
                'resource_name': 'trainings'})
        create_models('layer')
        for i in range(0, 10):
            training_factory()

    def test_training_browse(self):
        response = self.api_client.get(self.list_url)
        self.assertValidJSONResponse(response)
        self.assertEquals(len(self.deserialize(response)['objects']), 10)

    def test_keywords_filters(self):
        """Test keywords filtering"""

        from taggit.models import Tag
        for tag in Tag.objects.all():
            filter_url = self.list_url + '?keywords__slug__in=' + tag.name
            tagged_count = Training.objects.filter(
                keywords__name__in=[tag.name]).count()
            response = self.api_client.get(filter_url)
            self.assertValidJSONResponse(response)
            self.assertEquals(len(self.deserialize(response)['objects']), tagged_count)
