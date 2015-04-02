from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from taggit.managers import TaggableManager

from geonode.layers.models import Layer


class Training(models.Model):
    """
    A WFP training.
    A training consists of a manual and its associated layers
    """

    title = models.CharField(
        _('title'), max_length=255,
        help_text=_('name by which the cited manual is known'))
    logo = models.ImageField(upload_to="trainings/logos")
    manual = models.FileField(upload_to='trainings/manuals')
    publication_date = models.DateField(
        _('publication date'),
        help_text=_('publication date of the training'))
    layers = models.ManyToManyField(Layer, blank=True)
    abstract = models.TextField(
        _('abstract'), blank=True,
        help_text=_('brief narrative summary of the content of the training'))
    keywords = TaggableManager(
        _('keywords'), blank=True,
        help_text=_(
            'commonly used word(s) or formalised word(s) or phrase(s)'
            ' used to describe the subject (space or comma-separated')
        )

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'GIS Trainings'

    def get_absolute_url(self):
        return reverse('training_detail', args=(self.id,))

    def get_layers(self):
        layers = []
        for layer in self.layers.all():
            layers.append(layer.title)
        return ", ".join(layers)
    get_layers.short_description = 'Layers'
