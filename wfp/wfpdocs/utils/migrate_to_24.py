import psycopg2

from geonode.people.models import Profile
from geonode.base.models import Region

from wfp.wfpdocs.models import WFPDocument, Category

dbname = 'sdi_django'
host = 'localhost'
user = 'me'
password = 'mypassword'

conn = psycopg2.connect(
    "dbname='%s' user='%s' port='5432' host='%s' password='%s'" % (dbname, user, host, password)
)

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
where d.resourcebase_ptr_id < 1930 and d.resourcebase_ptr_id >= 1508
order by id
"""

cur = conn.cursor()
cur.execute(sql_wfpdocs)
rows = cur.fetchall()
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
    cur2 = conn.cursor()
    cur2.execute(sql_categories)
    rows2 = cur2.fetchall()
    for cat in rows2:
        cat_name = cat[0]
        print 'Adding %s category to static map' % cat_name
        category = Category.objects.get(name=cat_name)
        doc.categories.add(category)

    # 2. regions
    sql_regions = """
    select r.code, r.name from base_resourcebase_regions rbr
    join base_resourcebase rb
    on rbr.resourcebase_id = rb.id
    join base_region r
    on rbr.region_id = r.id
    where rb.id = %s
    """ % id
    cur3 = conn.cursor()
    cur3.execute(sql_regions)
    rows3 = cur3.fetchall()
    for reg in rows3:
        region_code = reg[0]
        region_name = reg[1]
        if Region.objects.filter(code=region_code).count() == 1:
            print 'Adding %s region' % region_name
            region = Region.objects.get(code=region_code)
            doc.regions.add(region)
        else:
            print 'It does not exist the region %s, %s' % (region_code, region_name)
    # 3. keywords
    sql_keywords = """
    select rb.id, t.name from taggit_taggeditem tt
    join base_resourcebase rb
    on tt.object_id = rb.id
    join taggit_tag t
    on tt.tag_id = t.id
    where tt.content_type_id = 58 and rb.id = %s
    """ % id
    # 4. TODO migrate POC metadata etc
    cur4 = conn.cursor()
    cur4.execute(sql_keywords)
    rows4 = cur4.fetchall()
    for key in rows4:
        keyword_name = key[1]
        doc.keywords.add(keyword_name)
