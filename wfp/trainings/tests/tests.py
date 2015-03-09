import StringIO

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from geonode.search.populate_search_test_data import create_models

from wfp.trainings.models import Training
from wfp.trainings.tests.fixtures import training_factory, get_random_date


class LayersTest(TestCase):

    def setUp(self):
        create_models('layer')

    def test_training_creation(self):
        """ Tests the creation of a training with some layers """

        title = 'Test Training with Layers'
        training = training_factory(title=title)
        self.assertEquals(Training.objects.get(pk=training.id).title, title)

    def test_document_details(self):
        """ Tests accessing the details view of a training """

        training = training_factory()

        c = Client()
        response = c.get(reverse('training_detail', args=(str(training.id),)))
        self.assertEquals(response.status_code, 200)

    def test_search(self):
        """ Tests accessing the html output of a keyword search """
        for i in range(0, 10):
            training_factory()

        c = Client()
        from taggit.models import Tag
        for tag in Tag.objects.all():
            tagged_count = Training.objects.filter(
                keywords__name__in=[tag.name]).count()
            response = c.get(reverse('trainings_browse') + tag.name)
            self.assertContains(
                response,
                '<p class="search-count">Total: %s</p>' % tagged_count,
                status_code=200
            )

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
