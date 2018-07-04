# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2012 OpenPlans
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

"""Utilities for managing GeoNode layers
"""

# Standard Modules
import logging
import re
import os
import glob
import sys
import tempfile
import psycopg2
from csvkit import sql
from csvkit import table
from osgeo import gdal

# Django functionality
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.conf import settings
from django.db.models import Q

# Geonode functionality
from geonode import GeoNodeException
from geonode.people.utils import get_valid_user
from geonode.layers.models import Layer, UploadSession
from geonode.base.models import Link, SpatialRepresentationType, TopicCategory, Region
from geonode.layers.models import shp_exts, csv_exts, vec_exts, cov_exts
from geonode.layers.metadata import set_metadata


from geonode.utils import http_client

import tarfile

from zipfile import ZipFile, is_zipfile

logger = logging.getLogger('geonode.layers.utils')

_separator = '\n' + ('-' * 100) + '\n'

def process_csv_file(absolute_base_file, table_name_temp, new_table, geom_table_name, geom_table_id, geom_table_columns, geom_table_geom):
    # Create table based on CSV
    import csv
    f = open(absolute_base_file, 'rb')
    no_header_row = False

    with open(absolute_base_file, 'rb') as csvfile:
        # get the type of delimiter
        dialect = csv.Sniffer().sniff(csvfile.read())

    try:
        csv_table = table.Table.from_csv(f, name=table_name_temp, no_header_row=no_header_row, delimiter=dialect.delimiter)
    except:
        status_code = '400'
        errormsgs_val = "Failed to create the table from CSV."
        return errormsgs_val, status_code


    for idx, column in enumerate(csv_table):
        column.name = slugify(unicode(column.name)).replace('-', '_')
        # Check if the selected value from the dropdown menu matches the first value of the CSV header
        if idx == 0:
            print ("column.name.strip()", column.name.strip())
            print ("geom_table_id.strip()", geom_table_id.strip())
            if column.name.strip() != geom_table_id.strip():
                errormsgs_val = "The selected value of Layer Type doesn't match the one of the imported layer."
                status_code = '400'
                return errormsgs_val, status_code
    # Check if there are added columns in the CSV
    if idx < 2:
        errormsgs_val = "The CSV has no added columns. Please add extra columns."
        status_code = '400'
        return errormsgs_val, status_code
    else:
        try:
            sql_table = sql.make_table(csv_table, table_name_temp)
            create_table_sql = sql.make_create_table_statement(sql_table, dialect="postgresql")
            create_table_sql = re.sub(r'VARCHAR\([0-9]*\)','VARCHAR(254)', create_table_sql)
        except:
            return None, str(sys.exc_info()[0])

        constr = "dbname='{dbname}' user='{user}' host='{host}' password='{password}'".format(** {
            'dbname': settings.DATABASES['uploaded']['NAME'],
            'user': settings.DATABASES['uploaded']['USER'],
            'host': settings.DATABASES['uploaded']['HOST'],
            'password': settings.DATABASES['uploaded']['PASSWORD']
        })
        conn = psycopg2.connect(constr)

        try:
            # Check if there is already a table with the same name
            cur = conn.cursor()

            sqlstr = "SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name='{new_table_name}');".format(** {
                'new_table_name': new_table
            })
            cur.execute(sqlstr)
            exists = cur.fetchone()[0]
            if exists:
                errormsgs_val = "There is already a layer with this name. Please choose another title."
                status_code = '400'
                return errormsgs_val, status_code

            #  If temporary table exists then drop it - the create it and add primary key
            cur.execute('DROP TABLE IF EXISTS %s CASCADE;' % table_name_temp)
            cur.execute(create_table_sql)
            conn.commit()
            sqlstr = "ALTER TABLE IF EXISTS {temp_table} ADD COLUMN fid SERIAL PRIMARY KEY;".format(** {
                'temp_table': table_name_temp
            })
            cur.execute(sqlstr)
            conn.commit()
        except Exception as e:
            logger.error(
                "Error Creating Temporary table %s:%s",
                table_name_temp,
                str(e))

        #  Copy data to table
        connection_string = "postgresql://%s:%s@%s:%s/%s" % (settings.DATABASES['uploaded']['USER'], settings.DATABASES['uploaded']['PASSWORD'], settings.DATABASES['uploaded']['HOST'], settings.DATABASES['uploaded']['PORT'], settings.DATABASES['uploaded']['NAME'])
        try:
            engine, metadata = sql.get_connection(connection_string)
        except ImportError:
            return None, str(sys.exc_info()[0])

        conn_eng = engine.connect()
        trans = conn_eng.begin()

        if csv_table.count_rows() > 0:
            insert = sql_table.insert()
            headers = csv_table.headers()
            try:
                conn_eng.execute(insert, [dict(zip(headers, row)) for row in csv_table.to_rows()])
            except:
                return None, str(sys.exc_info()[0])

        trans.commit()
        conn_eng.close()

        # Create joined table - drop table_name_temp
        new_clmns = []
        for idx, item in enumerate(headers):
            if (idx > 1):  # The downloaded layer contains two columns from the global table, which do not include them again
                new_column = "{table_name}.{item}".format(** {
                    'table_name': table_name_temp,
                    'item': item
                })
                new_clmns.append(new_column)

        added_columns = ', '.join(new_clmns)
        try:

            # Joined table
            sqlstr = "CREATE TABLE {new_table_name} AS (SELECT {geom_table_columns}, {added_columns} FROM {geom_table} INNER JOIN {temp_table} ON (g.{id} = {temp_table}.{id}));".format(** {
                'new_table_name': new_table,
                'geom_table': geom_table_name,
                'geom_table_columns': geom_table_columns,
                'temp_table': table_name_temp,
                'id': geom_table_id,
                'added_columns': added_columns
            })
            cur.execute(sqlstr)
            conn.commit()
            sqlstr = "ALTER TABLE IF EXISTS {new_table_name} ADD COLUMN fid SERIAL PRIMARY KEY;".format(** {
                'new_table_name': new_table
            })
            cur.execute(sqlstr)
            conn.commit()

            sqlstr = "CREATE INDEX indx_{new_table_name} ON {new_table_name} USING btree({id});".format(** {
                'new_table_name': new_table,
                'id': geom_table_id,
            })
            cur.execute(sqlstr)
            conn.commit()
            sqlstr = "CREATE INDEX indx_geom_{new_table_name} ON {new_table_name} USING GIST({geom});".format(** {
                'new_table_name': new_table,
                'geom': geom_table_geom,
            })
            cur.execute(sqlstr)
            conn.commit()

        except:
            print "Failed to create joined table."
            logger.error(
                "Failed to create joined table.")

        try:
            sqlstr = "DROP TABLE IF EXISTS {temp_table} CASCADE;".format(** {
                'temp_table': table_name_temp
            })
            cur.execute(sqlstr)
            conn.commit()
        except:
            logger.error(
                "Failed to drop temporary table.")
        conn.close()

        status_code = 200
        errormsgs_val = ''
        return errormsgs_val, status_code

def create_empty_layer(table_name, table_fields_list):

    try:

        constr = "dbname='{dbname}' user='{user}' host='{host}' password='{password}'".format(** {
            'dbname': settings.DATABASES['uploaded']['NAME'],
            'user': settings.DATABASES['uploaded']['USER'],
            'host': settings.DATABASES['uploaded']['HOST'],
            'password': settings.DATABASES['uploaded']['PASSWORD']
        })
        conn = psycopg2.connect(constr)
        cur = conn.cursor()

        sqlstr = "SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name='{table_name}');".format(** {
            'table_name': table_name
        })
        cur.execute(sqlstr)
        exists = cur.fetchone()[0]
        if exists:
            errormsgs_val = "There is already a layer with this name. Please choose another name."
            status_code = '400'
            return errormsgs_val, status_code

        sqlstr = "CREATE TABLE {table_name} ({table_fields_list}) ".format(** {
            'table_name': table_name,
            'table_fields_list': table_fields_list
        })

        cur.execute(sqlstr)
        conn.commit()

        sqlstr = "CREATE INDEX indx_geom_{table_name} ON {table_name} USING GIST({geom});".format(** {
            'table_name': table_name,
            'geom': 'the_geom'
        })

        cur.execute(sqlstr)
        conn.commit()

        status_code = 200
        errormsgs_val = ''
        return errormsgs_val, status_code
    except:

        status_code = 400
        errormsgs_val = 'Failed to create table'
        return errormsgs_val, status_code
