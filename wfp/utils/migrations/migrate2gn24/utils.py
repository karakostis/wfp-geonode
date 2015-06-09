import psycopg2

def get_src():
    """Get input db (GeoNode 2.0)"""
    dbname = 'sdi_django'
    host = 'localhost'
    user = 'me'
    password = 'mypassword'

    conn = psycopg2.connect(
        "dbname='%s' user='%s' port='5432' host='%s' password='%s'" % (dbname, user, host, password)
    )
    return conn


def get_dst():
    """Get output db (GeoNode 2.4)"""
    dbname = 'sdi_django_24'
    host = 'localhost'
    user = 'me'
    password = 'mypassword'

    conn = psycopg2.connect(
        "dbname='%s' user='%s' port='5432' host='%s' password='%s'" % (dbname, user, host, password)
    )
    return conn


def get_userid_by_oldid(id):
    """Get an username id by old id"""
    src = get_src()
    dst = get_dst()
    src_cur = src.cursor()
    src_cur.execute('SELECT username FROM auth_user WHERE id = %s;' % id)
    username = src_cur.next()[0]
    dst_cur = dst.cursor()
    dst_cur.execute("SELECT id FROM people_profile WHERE username = '%s';" % username)
    new_id = dst_cur.next()[0]
    print 'User id %s is now %s' % (id, new_id)
    return new_id


def get_resourceid_by_oldid(id):
    """Get an resource id by old id"""
    src = get_src()
    dst = get_dst()
    src_cur = src.cursor()
    src_cur.execute('SELECT uuid FROM base_resourcebase WHERE id = %s;' % id)
    if src_cur.rowcount == 0:
        return None
    uuid = src_cur.next()[0]
    dst_cur = dst.cursor()
    dst_cur.execute("SELECT id FROM base_resourcebase WHERE uuid = '%s';" % uuid)
    if dst_cur.rowcount == 0:
        return None
    new_id = dst_cur.next()[0]
    print 'Resource id %s is now %s' % (id, new_id)
    return new_id


def get_content_type_id_by_oldid(id):
    """Get content_type_id by old id"""
    src = get_src()
    dst = get_dst()
    src_cur = src.cursor()
    src_cur.execute('select app_label, model from django_content_type where id = %s;' % id)
    if src_cur.rowcount == 0:
        return None
    row = src_cur.next()
    app_label = row[0]
    model = row[1]
    dst_cur = dst.cursor()
    dst_cur.execute("select id from django_content_type where app_label = '%s' and model = '%s'" % (app_label, model))
    if dst_cur.rowcount == 0:
        return None
    new_id = dst_cur.next()[0]
    print 'Content type id %s is now %s' % (id, new_id)
    return new_id


def get_tag_id(slug):
    """Get tag id from tag slug"""
    dst = get_dst()
    dst_cur = dst.cursor()
    dst_cur.execute("SELECT id FROM taggit_tag WHERE slug = '%s';" % slug)
    if dst_cur.rowcount == 0:
        return None
    id = dst_cur.next()[0]
    print 'Tag id for %s is %s' % (slug, id)
    return id


def get_content_type_id(model):
    """Get content type id from model's name"""
    dst = get_dst()
    dst_cur = dst.cursor()
    dst_cur.execute("SELECT id FROM django_content_type WHERE model = '%s';" % model)
    id = dst_cur.next()[0]
    print 'Content type id for %s is %s' % (model, id)
    return id


def get_en_fields(id):
    """Get values for *_en fields"""
    dst = get_dst()
    dst_cur = dst.cursor()
    dst_cur.execute("SELECT title, abstract, purpose, constraints_other, supplemental_information, distribution_description, data_quality_statement FROM base_resourcebase WHERE id = %s" % id)
    en_fields = dst_cur.next()
    return en_fields


def get_permissions_dict():
    """Get auth permission id from code name"""
    dst = get_dst()
    dst_cur = dst.cursor()
    dst_cur.execute("SELECT codename, id from auth_permission;")
    permissions_dict = {}
    for row in dst_cur.fetchall():
        permissions_dict[row[0]] = row[1]
    return permissions_dict


def get_attributes_by_uuid(uuid, model):
    """Get attributes from layers/documents/maps for a given uuid"""
    src = get_src()
    src_cur = src.cursor()
    model_table = ''
    if model == 'layer':
        model_table = 'layers_layer'
    if model == 'map':
        model_table = 'maps_map'
    if model == 'document':
        model_table = 'documents_document'
    src_cur.execute("select popular_count, share_count from base_resourcebase rb join %s m on rb.id = m.resourcebase_ptr_id where uuid = '%s'" % (model_table, uuid))
    attributes = src_cur.next()
    return attributes
