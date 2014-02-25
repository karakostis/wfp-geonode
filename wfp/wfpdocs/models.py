from django.db import models
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
        (0, 'A0'),
        (1, 'A1'),
        (0, 'A2'),
        (1, 'A3'),
        (0, 'A4'),
    )

    source = models.CharField(max_length=255)
    orientation = models.IntegerField('Orientation', choices=ORIENTATION_CHOICES)
    format = models.IntegerField('Format', choices=FORMAT_CHOICES)
    document = models.OneToOneField(Document)
    categories = models.ManyToManyField(Category, verbose_name='categories', blank=True)

    def __str__(self):  
          return "%s" % self.source
