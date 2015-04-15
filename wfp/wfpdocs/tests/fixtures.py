import random

from django.contrib.auth.models import User
from django_dynamic_fixture import G
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.hashers import make_password

from geonode.people.models import Profile
from geonode.layers.models import Layer
from geonode.documents.models import Document

from wfp.wfpdocs.models import WFPDocument
from wfp.wfpdocs.models import Category


def rol_capooti():
    username = 'roland.capooti'
    if  Profile.objects.filter(username=username).count() == 1:
        return Profile.objects.get(username=username)
    else:
        return G(Profile, first_name='Roland', last_name='Capooti',
                 username=username, password=make_password('test'),
                 email='roland.capooti@wfp.org')


def doc_factory(**kwargs):
    """ Factory for a document """
    title = kwargs.pop('title', None)
    abstract = kwargs.pop('abstract', None)
    doc_number = random.randint(0, 1000)
    if not title:
        title = 'Document N. %s' % doc_number
    if not abstract:
        abstract = 'Abstract for document N. %s' % doc_number
    owner = rol_capooti()
    return G(Document, title=title, abstract=abstract,
             content_type=None, object_id=None, owner=owner)


def wfpdoc_factory(**kwargs):
    """ Factory for a static map """
    wfpdoc_number = random.randint(0, 1000)
    title = kwargs.pop('title', None)
    if not title:
        title = 'Static map N. %s' % wfpdoc_number
    abstract = 'Abstract for static map N. %s' % wfpdoc_number

    document = doc_factory(title=title, abstract=abstract)
    wfpdoc = G(WFPDocument, document=document)

    # associate a layer. TODO also associate maps in place of layers
    id_list = list(xrange(Layer.objects.all().count()))
    random.shuffle(id_list)
    layer = Layer.objects.all()[id_list[0]]
    layer_ct = ContentType.objects.get(app_label="layers", model="layer")
    wfpdoc.content_type = layer_ct
    wfpdoc.object_id = layer.id
    wfpdoc.save()

    # append some (0 to 3) categories
    id_list = list(xrange(Category.objects.all().count()))
    random.shuffle(id_list)
    for i in range(0, 3):
        category = Category.objects.all()[id_list[i]]
        wfpdoc.categories.add(category)

    return wfpdoc
