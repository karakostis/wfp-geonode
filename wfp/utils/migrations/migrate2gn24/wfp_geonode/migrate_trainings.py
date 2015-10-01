#!/usr/bin/python
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import utils

src = utils.get_src()
dst = utils.get_dst()

src_cur = src.cursor()
dst_cur = dst.cursor()

src_cur.execute("select title, logo, manual, publication_date, abstract from trainings_training")

for src_row in src_cur:
    assignments = []
    # title
    title = src_row[0]
    assignments.append(title)
    # logo
    assignments.append(src_row[1])
    # manual
    assignments.append(src_row[2])
    # publication_date
    assignments.append(src_row[3])
    # abstract
    assignments.append(src_row[4])

    try:
        print 'Migrating training %s' % title
        dst_cur.execute("insert into trainings_training (title, logo, manual, publication_date, abstract) values (%s, %s, %s, %s, %s)", assignments)
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
