import csv
import os

from geonode.base.models import Region
from geonode.layers.models import Layer

import os


def normalize_shapefile(shapefile):
    layername = shapefile.split('/')[-1][:-4]
    removefield_cmd = 'ogrinfo %s -sql "ALTER TABLE %s DROP COLUMN objectid"' % (shapefile, layername)
    os.system(removefield_cmd)
    print 'Shapefile %s normalized.' % shapefile

def run_importlayers(shapefile, user, keywords, category, regions):
    importlayers_cmd = 'python ./manage.py importlayers %s --user=ehab.elkhatib --category=%s  --regions="%s" --overwrite' % (shapefile, category, regions)
    print importlayers_cmd
    os.system(importlayers_cmd)
    layername = shapefile.split('/')[-1][:-4]
    typename = 'geonode:%s' % layername.lower()
    layer = Layer.objects.filter(typename=typename)[0]
    layer.title = title
    for keyword in keywords.split(','):
        layer.keywords.add(keyword)
    layer.save()

class2import = 'wfp'
workdir = '/tmp/cairo'

with open('%s/%s.csv' % (workdir, class2import), 'rb') as csvfile:
    count = 0
    reader = csv.reader(csvfile)
    for row in reader:
        layername = row[0]
        print 'Going to import %s' % layername
        shapefile = '/%s/%s/%s' % (workdir, class2import, layername)
        regions = row[2]
        title = row[1]
        if '%s' in title:
            main_region = Region.objects.filter(code=regions.split(',')[0])[0].name
            title = title % main_region
        category = row[3]
        keywords = row[4]
        normalize_shapefile(shapefile)
        run_importlayers(
                    shapefile=shapefile,
                    user='ehab.elkhatib',
                    keywords=keywords,
                    category=category,
                    regions=regions
                )
        print 'Finished import shapefile n. %s named %s' % (count, shapefile)
        count = count + 1
