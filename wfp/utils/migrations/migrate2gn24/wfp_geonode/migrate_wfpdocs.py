#!/usr/bin/python
import os, sys

path = os.path.dirname(__file__)
geonode_path = os.path.abspath(os.path.join(path, '../../../../..'))
sys.path.append(geonode_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wfp.settings._geonode24")

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import utils
from geonode.people.models import Profile
from geonode.base.models import Region, ResourceBase

from wfp.wfpdocs.models import WFPDocument, Category
from wfp.trainings.models import Training

src = utils.get_src()
dst = utils.get_dst()

src_cur = src.cursor()
src_cur2 = src.cursor()

def migrate_wfpdocs():
    sql_wfpdocs = """
    select d.resourcebase_ptr_id as id,
    b.title,
    b.date,
    w.page_format,
    w.orientation,
    w.source,
    d.doc_file,
    d.extension,
    d.popular_count,
    d.share_count,
    w.id as wfpdocument_id,
    b.uuid
    from wfpdocs_wfpdocument as w
    join documents_document as d
    on w.document_id = d.resourcebase_ptr_id
    join base_resourcebase as b
    on d.resourcebase_ptr_id = b.id
    order by id
    """

    WFPDocument.objects.all().delete()
    src_cur.execute(sql_wfpdocs)
    rows = src_cur.fetchall()
    for row in rows:
        # TODO real owner here
        profile = Profile.objects.all()[1]
        id = row[0]
        title = row[1]
        date = row[2]
        page_format = row[3]
        orientation = row[4]
        source = row[5]
        doc_file = row[6]
        extension = row[7]
        popular_count = row[8]
        share_count = row[9]
        wfpdocument_id = row[10]
        uuid = row[11]
        print id, title
        #import ipdb;ipdb.set_trace()
        # we need to remove existing doc, created from the migration process
        try:
            ResourceBase.objects.get(uuid=uuid).delete()
        except Exception as error:
            pass
        doc = WFPDocument()
        doc.title = title
        doc.owner = profile
        doc.slug = id
        doc.date = date
        doc.page_format = page_format
        doc.orientation = orientation
        doc.source = source
        doc.doc_file = doc_file
        doc.popular_count = popular_count
        doc.share_count = share_count
        doc.uuid = uuid
        doc.save()
        # 1. categories
        sql_categories = """
        select name from wfpdocs_wfpdocument_categories as wc
        join wfpdocs_category as c
        on wc.category_id = c.id
        where wfpdocument_id = %s
        """ % wfpdocument_id
        src_cur2.execute(sql_categories)
        rows2 = src_cur2.fetchall()
        for cat in rows2:
            cat_name = cat[0]
            print 'Adding %s category to static map' % cat_name
            category = Category.objects.get(name=cat_name)
            doc.categories.add(category)

migrate_wfpdocs()
