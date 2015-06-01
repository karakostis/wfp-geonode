import random
import StringIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.hashers import make_password

from django_dynamic_fixture import G

from geonode.people.models import Profile
from geonode.layers.models import Layer

from wfp.wfpdocs.models import WFPDocument
from wfp.wfpdocs.models import Category


def rol_capooti():
    """ Factory for a sample user """
    username = 'roland.capooti'
    if Profile.objects.filter(username=username).count() == 1:
        return Profile.objects.get(username=username)
    else:
        return G(Profile, first_name='Roland', last_name='Capooti',
                 username=username, password=make_password('test'),
                 email='roland.capooti@wfp.org')


def wfpdoc_factory(**kwargs):
    """ Factory for a static map """
    # it seems we cannot use django-dynamic-fixtures with django-polymorphic
    # therefore we create the fixture the old fashion way
    wfpdoc_number = random.randint(0, 1000)
    title = kwargs.pop('title', None)
    if not title:
        title = 'Static map N. %s' % wfpdoc_number
    abstract = 'Abstract for static map N. %s' % wfpdoc_number
    # we need to upload a file
    imgfile = StringIO.StringIO(
            'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00'
            '\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;')
    doc_file = SimpleUploadedFile(
            '%s.gif' % wfpdoc_number,
            imgfile.read(),
            'image/gif')
    owner = rol_capooti()
    wfpdoc = WFPDocument(title=title, abstract=abstract, owner=owner, doc_file=doc_file)
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

    # set permissions
    perm_spec = {
        "users": {
            "admin": [
                "change_resourcebase",
                "change_resourcebase_permissions",
                "view_resourcebase"]},
        "groups": {}}
    wfpdoc.set_permissions(perm_spec)

    return wfpdoc
