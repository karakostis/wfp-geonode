import StringIO

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from geonode.search.populate_search_test_data import create_models

from wfp.wfpdocs.models import WFPDocument
from wfp.wfpdocs.tests.fixtures import wfpdoc_factory


class WFPDocTest(TestCase):

    def setUp(self):
        create_models('layer')

    def test_wfpdoc_creation(self):
        """ Tests the creation of a static map """

        title = 'Test static map with layers'
        wfpdoc = wfpdoc_factory(title=title)
        self.assertEquals(
            WFPDocument.objects.get(pk=wfpdoc.id).document.title, title)

    def test_wfpdoc_details(self):
        """ Tests accessing the details view of a static map """

        wfpdoc = wfpdoc_factory()

        response = self.client.get(
            reverse('wfpdocs-detail', args=(str(wfpdoc.document.id),)))

        # by default anonymous access is forbidden
        self.assertEquals(response.status_code, 403)

        # now login
        # TODO when moving to 2.4, test django guardian permissions
        self.client.login(username='admin', password='admin')
        response = self.client.get(
            reverse('wfpdocs-detail', args=(str(wfpdoc.document.id),)))
        self.assertEquals(response.status_code, 200)

    def test_wfpdoc_upload(self):
        """ Tests uploading a new static map """

        staticmap_file = StringIO.StringIO(
            'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00'
            '\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;')
        staticmap = SimpleUploadedFile(
            'staticmap_test_file.gif', staticmap_file.read(), 'image/gif')

        self.client.login(username='admin', password='admin')
        perms = """
            {"anonymous":"_none","authenticated":"document_readonly","users":[]}
            """
        response = self.client.post(
            reverse('wfpdocs-upload'),
            data={
                    'title': 'Uploaded Static Map',
                    'file': staticmap,
                    'source': 'WFP GIS',
                    'orientation': WFPDocument.ORIENTATION_CHOICES[0][0],
                    'page_format': WFPDocument.FORMAT_CHOICES[0][0],
                    'publication_date_0': '2015-03-09',
                    'publication_date_1': '18:10:17',
                    'resource': 'no_link',
                    'last_version': 'on',
                    'permissions': perms
                 },
            follow=True)

        self.assertEquals(WFPDocument.objects.all().count(), 1)

        wfpdoc = WFPDocument.objects.all()[0]
        # authenticate user must get 200 when visiting details page
        response = self.client.get(
            reverse('wfpdocs-detail',
                    args=(str(wfpdoc.document.id),)))
        self.assertEquals(response.status_code, 200)
        # unauthenticated user must get 403 when visiting details page
        self.client.logout()
        response = self.client.get(
            reverse('wfpdocs-detail',
                    args=(str(wfpdoc.document.id),)))
        self.assertEquals(response.status_code, 403)

    def test_wfpdocs_rss(self):
        """ Tests RSS feed"""

        import feedparser
        # we test feed with 10 entries, 5 being public
        for i in range(0, 10):
            wfpdoc = wfpdoc_factory()
            if i > 4:
                wfpdoc.document.set_default_permissions()

        feed = feedparser.parse(
            self.client.get(reverse('wfpdocs-rss')).content)

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

        # anonymous can go to wfpdocs-browse
        response = self.client.get(reverse('wfpdocs-browse'))
        self.assertEqual(200, response.status_code)

        # anonymous going go wfpdocs-upload must be redirected to login
        response = self.client.get(reverse('wfpdocs-upload'))
        self.assertEqual(302, response.status_code)

        # authenticated can go to wfpdocs-upload
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('wfpdocs-upload'))
        self.assertEqual(200, response.status_code)
        self.client.logout()

        # let's create a static map, and test static map detail and remove page
        wfpdoc = wfpdoc_factory()

        # anonymous goint to wfpdocs-detail is not authorized
        response = self.client.get(
            reverse('wfpdocs-detail', args=(str(wfpdoc.document.id),)))
        self.assertEqual(403, response.status_code)

        # authenticated can go to wfpdocs-detail
        self.client.login(username='admin', password='admin')
        response = self.client.get(
            reverse('wfpdocs-detail', args=(str(wfpdoc.document.id),)))
        self.assertEqual(200, response.status_code)
        self.client.logout()

        # anonymous goint to wfpdocs-update must be redirected to login
        response = self.client.get(
            reverse('wfpdocs-update', args=(str(wfpdoc.id),)))
        self.assertEqual(302, response.status_code)

        # static map owner can go to wfpdocs-update
        self.client.login(username='roland.capooti', password='test')
        response = self.client.get(
            reverse('wfpdocs-update', args=(str(wfpdoc.id),)))
        self.assertEqual(200, response.status_code)
        self.client.logout()

        # anonymous goint to wfpdocs-remove must be redirected to login
        response = self.client.get(
            reverse('wfpdocs-remove', args=(str(wfpdoc.document.id),)))
        self.assertEqual(302, response.status_code)

        # static map owner can go to wfpdocs-remove
        self.client.login(username='roland.capooti', password='test')
        response = self.client.get(
            reverse('wfpdocs-remove', args=(str(wfpdoc.document.id),)))
        self.assertEqual(200, response.status_code)
        self.client.logout()

        # anonymous can go to wfpdocs-rss
        response = self.client.get(reverse('wfpdocs-rss'))
        self.assertEqual(200, response.status_code)
