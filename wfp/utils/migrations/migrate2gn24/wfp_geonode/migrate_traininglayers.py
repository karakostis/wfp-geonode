#!/usr/bin/python
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import utils

def get_trainingid_by_oldid(id):
    """Get a training id by old id"""
    src = utils.get_src()
    dst = utils.get_dst()
    src_cur = src.cursor()
    src_cur.execute('select title from trainings_training WHERE id = %s;' % id)
    title = src_cur.next()[0]
    dst_cur = dst.cursor()
    dst_cur.execute("SELECT id FROM trainings_training WHERE title = '%s';" % title)
    new_id = dst_cur.next()[0]
    print 'Training id %s is now %s' % (id, new_id)
    return new_id

src = utils.get_src()
dst = utils.get_dst()

src_cur = src.cursor()
dst_cur = dst.cursor()

src_cur.execute("select training_id, layer_id from trainings_training_layers")

for src_row in src_cur:
    assignments = []
    # training_id
    assignments.append(get_trainingid_by_oldid(src_row[0]))
    # layer_id
    assignments.append(utils.get_resourceid_by_oldid(src_row[1]))

    try:
        dst_cur.execute("insert into trainings_training_layers (training_id, layer_id) values (%s, %s)", assignments)
        dst.commit()
    except Exception as error:
        print 
        print type(error)
        print str(src_row)
        dst.rollback()

src_cur.close()
dst_cur.close()
src.close()
dst.close()
