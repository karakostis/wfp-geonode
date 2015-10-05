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
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from geonode.layers.models import Layer
from geonode.base.populate_test_data import create_models

from wfp.wfpdocs.models import WFPDocument
from wfp.wfpdocs.tests.fixtures import wfpdoc_factory


if 'geonode.geoserver' in settings.INSTALLED_APPS:
    from django.db.models import signals
    from geonode.geoserver.signals import geoserver_pre_save
    from geonode.geoserver.signals import geoserver_post_save
    signals.pre_save.disconnect(geoserver_pre_save, sender=Layer)
    signals.post_save.disconnect(geoserver_post_save, sender=Layer)


class WFPDocTest(TestCase):

    def setUp(self):
        create_models(type='layer')

    def test_wfpdoc_creation(self):
        """ Tests the creation of a static map """

        title = 'Test static map with layers'
        wfpdoc = wfpdoc_factory(title=title)
        self.assertEquals(
            WFPDocument.objects.get(pk=wfpdoc.id).title, title)

    def test_wfpdoc_details(self):
        """ Tests accessing the details view of a static map """

        wfpdoc = wfpdoc_factory()

        response = self.client.get(
            reverse('wfpdocs_detail', args=(str(wfpdoc.slug),)))

        # by default anonymous access is forbidden
        self.assertEquals(response.status_code, 403)

        # now login
        # TODO when moving to 2.4, test django guardian permissions
        self.client.login(username='admin', password='admin')
        response = self.client.get(
            reverse('wfpdocs_detail', args=(str(wfpdoc.slug),)))
        self.assertEquals(response.status_code, 200)

    def test_wfpdoc_upload(self):
        """ Tests uploading a new static map """

        staticmap_file = StringIO.StringIO(
            'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00'
            '\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;')
        staticmap = SimpleUploadedFile(
            'staticmap_test_file.gif', staticmap_file.read(), 'image/gif')

        self.client.login(username='admin', password='admin')
        response = self.client.post(
            reverse('wfpdocs_upload'),
            data={
                    'title': 'Uploaded Static Map',
                    'doc_file': staticmap,
                    'source': 'WFP GIS',
                    'orientation': WFPDocument.ORIENTATION_CHOICES[0][0],
                    'page_format': WFPDocument.FORMAT_CHOICES[0][0],
                    'date': '2015-10-02',
                    'resource': 'no_link',
                    'last_version': 'on',
                    'permissions': '{"users":{"AnonymousUser": []}}'
                 },
            follow=True)
        self.assertEquals(WFPDocument.objects.all().count(), 1)

        wfpdoc = WFPDocument.objects.all()[0]
        # authenticate user must get 200 when visiting details page
        response = self.client.get(
            reverse('wfpdocs_detail',
                    args=(str(wfpdoc.slug),)))
        self.assertEquals(response.status_code, 200)
        # unauthenticated user must get 403 when visiting details page
        self.client.logout()
        response = self.client.get(
            reverse('wfpdocs_detail',
                    args=(str(wfpdoc.slug),)))
        self.assertEquals(response.status_code, 403)

    def test_wfpdocs_rss(self):
        """ Tests RSS feed"""

        import feedparser
        # we test feed with 10 entries, 5 being public
        for i in range(0, 10):
            wfpdoc = wfpdoc_factory()
            if i > 4:
                wfpdoc.set_default_permissions()

        feed = feedparser.parse(
            self.client.get(reverse('wfpdocs_rss')).content)

        # feed must have only 5 entries (one for each of the 5 public maps)
        self.assertEqual(len(feed.entries), 5)
        # check feed title
        from wfp.wfpdocs.feeds import WFPDocumentsFeed
        self.assertEqual(feed['feed']['title'], WFPDocumentsFeed.title)

    def test_wfpdocs_api(self):
        # TODO
        pass

    def test_pages_render(self):
        """
        Verify pages that do and do not require login and corresponding status
        codes
        """

        # anonymous can go to wfpdocs_browse
        response = self.client.get(reverse('wfpdocs_browse'))
        self.assertEqual(200, response.status_code)

        # anonymous going go wfpdocs_upload must be redirected to login
        response = self.client.get(reverse('wfpdocs_upload'))
        self.assertEqual(302, response.status_code)

        # authenticated can go to wfpdocs_upload
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('wfpdocs_upload'))
        self.assertEqual(200, response.status_code)
        self.client.logout()

        # let's create a static map, and test static map detail and remove page
        wfpdoc = wfpdoc_factory()

        # anonymous going to wfpdocs_detail is not authorized
        response = self.client.get(
            reverse('wfpdocs_detail', args=(str(wfpdoc.slug),)))
        self.assertEqual(403, response.status_code)

        # authenticated can go to wfpdocs_detail
        self.client.login(username='admin', password='admin')
        response = self.client.get(
            reverse('wfpdocs_detail', args=(str(wfpdoc.slug),)))
        self.assertEqual(200, response.status_code)
        self.client.logout()

        # anonymous going to wfpdocs_update must be redirected to login
        response = self.client.get(
            reverse('wfpdocs_update', args=(str(wfpdoc.slug),)))
        self.assertEqual(302, response.status_code)

        # static map owner can go to wfpdocs_update
        self.client.login(username='roland.capooti', password='test')
        response = self.client.get(
            reverse('wfpdocs_update', args=(str(wfpdoc.slug),)))
        self.assertEqual(200, response.status_code)
        self.client.logout()

        # anonymous goint to wfpdocs_remove must be redirected to login
        response = self.client.get(
            reverse('wfpdocs_remove', args=(str(wfpdoc.slug),)))
        self.assertEqual(302, response.status_code)

        # static map owner can go to wfpdocs_remove
        self.client.login(username='roland.capooti', password='test')
        response = self.client.get(
            reverse('wfpdocs_remove', args=(str(wfpdoc.slug),)))
        self.assertEqual(200, response.status_code)
        self.client.logout()

        # anonymous can go to wfpdocs_rss
        response = self.client.get(reverse('wfpdocs_rss'))
        self.assertEqual(200, response.status_code)
