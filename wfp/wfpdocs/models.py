from django.db import models
from django.core.urlresolvers import reverse

from geonode.documents.models import Document

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
        
class WFPDocument(models.Model):
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
    document = models.OneToOneField(Document)
    categories = models.ManyToManyField(Category, verbose_name='categories', blank=True)
    last_version = models.BooleanField(default=False)
    date_updated = models.DateTimeField(auto_now=True, blank=False, null=False)

    def __str__(self):  
          return "%s" % self.source
    
    def get_absolute_url(self):
        return reverse('wfpdocs-detail', args=(self.document.id,))
        
    def get_file_size(self):
        try:
            num = self.document.doc_file.size
            for x in ['bytes','KB','MB','GB','TB']:
                if num < 1024.0:
                    return "%3.1f %s" % (num, x)
                num /= 1024.0
        except:
            return 0
            
    def get_regions(self):
        regions = []
        for region in self.document.regions.all():
            regions.append(region.name)
        return ", ".join(regions )
    get_regions.short_description = 'Regions'
    
    def get_date(self):
        return self.document.date.isoformat()
    get_date.short_description = 'Date'
    
    def get_categories(self):
        categories = []
        for category in self.categories.all():
            categories.append(category.name)
        return ", ".join(categories)
    get_categories.short_description = 'Categories'
    
    def get_date_type(self):
        return self.document.date_type
    get_date_type.short_description = 'Date Type'
    
    @property
    def class_name(self):
        return self.__class__.__name__
    
