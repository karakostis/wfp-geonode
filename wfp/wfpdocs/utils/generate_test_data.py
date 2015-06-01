from django.core.files import File
from random import randint

from geonode.documents.models import Document
from geonode.people.models import Profile
from geonode.base.models import TopicCategory


def create_document(number):
    print 'Generating image %s' % number
    admin = Profile.objects.filter(username='admin')[0]

    file_list = (
                    '1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg', '7.jpg',
                    '8.jpg', '9.png', '10.jpg', '11.jpg',)
    random_index = randint(0, 10)
    file_uri = '/home/capooti/Desktop/maps/%s' % file_list[random_index]
    title = 'Document N. %s' % number
    img_filename = '%s_img.jpg' % number

    doc = Document(title=title, owner=admin)
    doc.save()
    with open(file_uri, 'r') as f:
        img_file = File(f)
        doc.doc_file.save(img_filename, img_file, True)

    base = doc.get_self_resource()
    random_index = randint(0, 18)
    tc = TopicCategory.objects.all()[random_index]
    base.category = tc
    base.save()


for i in range(790, 5000):
    create_document(i)
