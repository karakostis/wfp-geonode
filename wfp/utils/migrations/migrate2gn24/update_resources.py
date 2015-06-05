from geonode.maps.models import Map
from geonode.documents.models import Document

for m in Map.objects.all():
    print 'Updating map %s' % m.title
    m.save()

for d in Document.objects.all():
    print 'Updating document %s' % d.title
    d.save()
