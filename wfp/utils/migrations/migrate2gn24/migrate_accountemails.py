#!/usr/bin/python
import utils

src = utils.get_src()
dst = utils.get_dst()

src_cur = src.cursor()
dst_cur = dst.cursor()

src_cur.execute("select user_id, email, verified, \"primary\" from account_emailaddress")

for src_row in src_cur:
  assignments = []
  #user_id
  assignments.append(utils.get_userid_by_oldid(src_row[0]))
  #email
  assignments.append(src_row[1])
  #verified
  assignments.append(src_row[2])
  #primary
  assignments.append(src_row[3])
  
  try:
    dst_cur.execute("insert into account_emailaddress(user_id, email, verified, \"primary\") values (%s, %s, %s, %s)", assignments)
    dst.commit()
  except Exception as error:
    print 
    print type(error)
    print str(error) + "select id, user_id, email, verified, \"primary\" from account_emailaddress"
    print str(src_row)
    dst.rollback()

src_cur.close()
dst_cur.close()
src.close()
dst.close()
