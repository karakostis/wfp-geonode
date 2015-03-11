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
