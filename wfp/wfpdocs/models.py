import os
import datetime
import logging

from django.conf import settings
from django.db import models
from django.db.models import signals
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.staticfiles import finders

from geonode.base.models import ResourceBase, resourcebase_post_save

IMGTYPES = ['jpg', 'jpeg', 'tif', 'tiff', 'png', 'gif']

logger = logging.getLogger(__name__)

class Category(models.Model):
    """
    A WFM Map Document category
    """
    
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
        
class WFPDocument(ResourceBase):
    """
    A WFP document
    """
    
    ORIENTATION_CHOICES = (
        (0, 'Landscape'),
        (1, 'Portrait'),
    )
    
    FORMAT_CHOICES = (
        (4, 'A4'),
        (0, 'A0'),
        (1, 'A1'),
        (2, 'A2'),
        (3, 'A3'),
    )

    source = models.CharField(max_length=255)
    orientation = models.IntegerField('Orientation', choices=ORIENTATION_CHOICES)
    page_format = models.IntegerField('Format', choices=FORMAT_CHOICES)
    #document = models.OneToOneField(Document)
    doc_file = models.FileField(upload_to='documents', max_length=255, verbose_name=_('File'))
    extension = models.CharField(max_length=128, blank=True, null=True)
    last_version = models.BooleanField(default=False)
    date_updated = models.DateTimeField(auto_now=True, blank=False, null=False)
    slug = models.SlugField()
    categories = models.ManyToManyField(Category, verbose_name='categories', blank=True)

    def __str__(self):  
          return "%s" % self.source
    
    def get_absolute_url(self):
        return reverse('wfpdocs-detail', args=(self.slug,))
        
    def get_file_size(self):
        try:
            num = self.doc_file.size
            for x in ['bytes','KB','MB','GB','TB']:
                if num < 1024.0:
                    return "%3.1f %s" % (num, x)
                num /= 1024.0
        except:
            return 0
            
    def get_regions(self):
        regions = []
        for region in self.regions.all():
            regions.append(region.name)
        return ", ".join(regions )
    get_regions.short_description = 'Regions'
    
    def get_categories(self):
        categories = []
        for category in self.categories.all():
            categories.append(category.name)
        return ", ".join(categories)
    get_categories.short_description = 'Categories'
    
    @property
    def class_name(self):
        return self.__class__.__name__
    
    def _render_thumbnail(self):
        from cStringIO import StringIO

        size = 200, 150

        try:
            from PIL import Image, ImageOps
        except ImportError, e:
            logger.error(
                '%s: Pillow not installed, cannot generate thumbnails.' %
                e)
            return None

        try:
            # if wand is installed, than use it for pdf thumbnailing
            from wand import image
        except:
            wand_available = False
        else:
            wand_available = True

        if wand_available and self.extension and self.extension.lower(
        ) == 'pdf' and self.doc_file:
            logger.debug(
                u'Generating a thumbnail for document: {0}'.format(
                    self.title))
            with image.Image(filename=self.doc_file.path) as img:
                img.sample(*size)
                return img.make_blob('png')
        elif self.extension and self.extension.lower() in IMGTYPES and self.doc_file:

            img = Image.open(self.doc_file.path)
            img = ImageOps.fit(img, size, Image.ANTIALIAS)
        else:
            filename = finders.find('documents/{0}-placeholder.png'.format(self.extension), False) or \
                finders.find('documents/generic-placeholder.png', False)

            if not filename:
                return None

            img = Image.open(filename)

        imgfile = StringIO()
        img.save(imgfile, format='PNG')
        return imgfile.getvalue()
    
def pre_save_wfpdocument(instance, sender, **kwargs):
    base_name, extension, doc_type = None, None, None
    base_name, extension = os.path.splitext(instance.doc_file.name)
    instance.extension = extension[1:]
    doc_type_map = settings.DOCUMENT_TYPE_MAP
    if doc_type_map is None:
        doc_type = 'other'
    else:
        if instance.extension in doc_type_map:
            doc_type = doc_type_map[''+instance.extension]
        else:
            doc_type = 'other'
    instance.doc_type = doc_type

    if not instance.uuid:
        instance.uuid = str(uuid.uuid1())

    
def create_thumbnail(sender, instance, created, **kwargs):
    from .tasks import create_wfpdoc_thumbnail

    create_wfpdoc_thumbnail.delay(object_id=instance.id)

signals.pre_save.connect(pre_save_wfpdocument, sender=WFPDocument)
signals.post_save.connect(create_thumbnail, sender=WFPDocument)
signals.post_save.connect(resourcebase_post_save, sender=WFPDocument)
