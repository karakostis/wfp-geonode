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

import os
import re
import sys
import csv
import logging
import shutil
import traceback
import requests
import psycopg2
from osgeo import ogr
from unidecode import unidecode
from owslib.wfs import WebFeatureService
from guardian.shortcuts import get_perms
from geoserver.catalog import Catalog


from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.utils.translation import ugettext as _
from django.utils import simplejson as json
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.template.defaultfilters import slugify
from django.forms.models import inlineformset_factory

from geonode.base.enumerations import CHARSETS
from geonode.security.views import _perms_info_json
from geonode.geoserver.helpers import gs_slurp
from geonode.geoserver.signals import geoserver_post_save

from wfp.create_layers.forms import UploadCSVForm, UploadEmptyLayerForm
from wfp.create_layers.utils import process_csv_file, create_empty_layer


@login_required
def layer_create(request, template='create_layers/layer_create.html'):

    if request.method == 'GET':
        ctx = {
            'charsets': CHARSETS,
            "is_layer": True,
        }

        # Get the values for the dropdown menus of regions and provinces
        constr = "dbname='{dbname}' user='{user}' host='{host}' password='{password}'".format(** {
            'dbname': settings.DATABASES['uploaded']['NAME'],
            'user': settings.DATABASES['uploaded']['USER'],
            'host': settings.DATABASES['uploaded']['HOST'],
            'password': settings.DATABASES['uploaded']['PASSWORD']
        })

        conn = psycopg2.connect(constr)
        cur = conn.cursor()

        sqlstr = "SELECT DISTINCT adm0_name FROM wld_bnd_adm0_gaul_2015 ORDER BY adm0_name;"
        cur.execute(sqlstr)
        countries = cur.fetchall()
        countries = [c[0] for c in countries]
        ctx['countries'] = countries

        form_csv_layer = UploadCSVForm()
        form_empty_layer = UploadEmptyLayerForm()
        ctx['form_csv_layer'] = form_csv_layer
        ctx['form_empty_layer'] = form_empty_layer
        return render_to_response(template, RequestContext(request, ctx))

    elif request.method == 'POST':

        # Get the values for the dropdown menus of regions and provinces
        ctx = {}
        constr = "dbname='{dbname}' user='{user}' host='{host}' password='{password}'".format(** {
            'dbname': settings.DATABASES['uploaded']['NAME'],
            'user': settings.DATABASES['uploaded']['USER'],
            'host': settings.DATABASES['uploaded']['HOST'],
            'password': settings.DATABASES['uploaded']['PASSWORD']
        })

        conn = psycopg2.connect(constr)
        cur = conn.cursor()

        sqlstr = "SELECT DISTINCT adm0_name FROM wld_bnd_adm0_gaul_2015 ORDER BY adm0_name;"
        cur.execute(sqlstr)
        countries = cur.fetchall()
        countries = [c[0] for c in countries]
        ctx['countries'] = countries

        if 'fromlayerbtn' in request.POST:
            the_user = request.user
            form_csv_layer = UploadCSVForm(request.POST, request.FILES)
            form_empty_layer = UploadEmptyLayerForm(request.POST, request.FILES)

            errormsgs = []
            ctx['success'] = False

            if form_csv_layer.is_valid():
                try:
                    title = form_csv_layer.cleaned_data["title"]

                    permissions = form_csv_layer.cleaned_data["permissions_json"]

                    layer_based_info = {
                        "1": {
                            "geom_table": "wld_bnd_adm0_gaul_2015 AS g",
                            "id": "adm0_code",
                            "columns": "g.adm0_code, g.adm0_name, g.the_geom",
                            "geom": "the_geom"
                            },
                        "2": {
                            "geom_table": "wld_bnd_adm1_gaul_2015 AS g",
                            "id": "adm1_code",
                            "columns": "g.adm0_code, g.adm0_name, g.adm1_code, g.adm1_name, g.the_geom",
                            "geom": "the_geom"
                            },
                        "3": {
                            "geom_table": "wld_bnd_adm2_gaul_2015 AS g",
                            "id": "adm2_code",
                            "columns": "g.adm0_code, g.adm0_name, g.adm1_code, g.adm1_name, g.adm2_code, g.adm2_name, g.the_geom",
                            "geom": "the_geom"
                            }
                    }

                    layer_type = form_csv_layer.cleaned_data["layer_type"]

                    geom_table_name = layer_based_info[layer_type[0]]['geom_table']
                    geom_table_id = layer_based_info[layer_type[0]]['id']
                    geom_table_geom = layer_based_info[layer_type[0]]['geom']
                    geom_table_columns = layer_based_info[layer_type[0]]['columns']
                    selected_country = form_csv_layer.cleaned_data["selected_country"]
                    cntr_name = slugify(selected_country[0].replace(" ", "_"))
                    slugified_title = slugify(title.replace(" ", "_"))
                    table_name_temp = "%s_%s_temp" % (cntr_name, slugified_title)
                    table_name = "%s_%s" % (cntr_name, slugified_title)
                    table_name_temp = table_name_temp
                    new_table = table_name

                    print ("title", title)
                    # Write CSV in the server
                    tempdir, absolute_base_file = form_csv_layer.write_files()

                    errormsgs_val, status_code = process_csv_file(absolute_base_file, table_name_temp, new_table, geom_table_name, geom_table_id, geom_table_columns, geom_table_geom)

                    if status_code == '400':
                        errormsgs.append(errormsgs_val)
                        ctx['errormsgs'] = errormsgs
                        return render_to_response(template, RequestContext(request, {'form_csv_layer': form_csv_layer, 'form_empty_layer': form_empty_layer, 'countries': countries, 'errormsgs': errormsgs, 'status_msg': json.dumps('400_csv'), "is_layer": True}))

                    # Create layer in geoserver
                    sld_style = 'polygon_style.sld'
                    _create_geoserver_geonode_layer(new_table, sld_style, title, the_user, permissions)

                    ctx['success'] = True

                except Exception as e:
                    ctx['success'] = False
                    ctx['errors'] = str(e)

                finally:
                    if tempdir is not None:
                        shutil.rmtree(tempdir)

                if ctx['success']:
                    status_code = 200
                    layer = 'geonode:' + new_table

                    return HttpResponseRedirect(
                        reverse(
                            'layer_metadata',
                            args=(
                                layer,
                            )))
            else:

                for e in form_csv_layer.errors.values():
                    errormsgs.append([escape(v) for v in e])

                ctx['errors'] = form_csv_layer.errors
                ctx['errormsgs'] = errormsgs
                ctx['success'] = False
                return render_to_response(template, RequestContext(request, {'form_csv_layer': form_csv_layer, 'form_empty_layer': form_empty_layer, 'countries': countries, 'status_msg': json.dumps('400_csv'), "is_layer": True}))


        elif 'emptylayerbtn' in request.POST:

            the_user = request.user
            ctx = {}
            form_csv_layer = UploadCSVForm(request.POST, request.FILES)
            form_empty_layer = UploadEmptyLayerForm(request.POST, extra=request.POST.get('total_input_fields'))

            errormsgs = []
            ctx['success'] = False

            if form_empty_layer.is_valid():

                field_types_info = {
                    "Integer": "integer",
                    "Character": "character varying(254)",
                    "Double": "double precision"
                }

                create_empty_layer_data = form_empty_layer.cleaned_data
                title = create_empty_layer_data['empty_layer_name']
                permissions = form_empty_layer.cleaned_data["permissions_json"]

                table_name = (create_empty_layer_data['empty_layer_name'].lower()).replace(" ", "_")
                # check table name for special characters
                if not re.match("^[\w\d_]+$", table_name) or table_name[0].isdigit():
                    status_code = '400'
                    errormsgs_val = "Not valid name for layer name. Use only characters or numbers for a name. Name can not start with a number."
                    errormsgs.append(errormsgs_val)
                    ctx['errormsgs'] = errormsgs
                    return render_to_response(template, RequestContext(request, {'form_csv_layer': form_csv_layer, 'form_empty_layer': form_empty_layer, 'countries': countries, 'errormsgs': errormsgs, 'status_msg': json.dumps('400_empty_layer'), "is_layer": True}))

                table_geom = create_empty_layer_data['geom_type']

                table_fields_list = ['fid serial NOT NULL']

                create_empty_layer_data_lngth = (len(create_empty_layer_data) - 3)/2  # need only field names and types divided by 2
                # check if user has added at least one column
                if (int(create_empty_layer_data['total_input_fields']) < 1):
                    status_code = '400'
                    if status_code == '400':
                        errormsgs_val = "You haven't added any additional columns. At least one column is required."
                        errormsgs.append(errormsgs_val)
                        ctx['errormsgs'] = errormsgs
                        return render_to_response(template, RequestContext(request, {'form_csv_layer': form_csv_layer, 'form_empty_layer': form_empty_layer, 'countries': countries, 'errormsgs': errormsgs, 'status_msg': json.dumps('400_empty_layer'), "is_layer": True}))

                field_types = []
                for key in create_empty_layer_data:
                    for i in range(create_empty_layer_data_lngth):
                        if key.startswith("extra_field_%s" % i):

                            field_name = create_empty_layer_data['extra_field_%s' % i].replace(" ", "_")

                            # check if string has special characters
                            if not re.match("^[\w\d_]+$", field_name) or field_name[0].isdigit():
                                status_code = '400'
                                errormsgs_val = "Not valid naming for attributes. Use only characters or numbers for a name. Name can not start with a number."
                                errormsgs.append(errormsgs_val)
                                ctx['errormsgs'] = errormsgs
                                return render_to_response(template, RequestContext(request, {'form_csv_layer': form_csv_layer, 'form_empty_layer': form_empty_layer, 'countries': countries, 'errormsgs': errormsgs, 'status_msg': json.dumps('400_empty_layer'), "is_layer": True}))

                            field_type_short = create_empty_layer_data['field_type_%s' % i] # get field type for this field name

                            field_type = field_types_info[field_type_short] # build the complete field type

                            field_name_type = field_name + " " + field_type
                            field_types.append(field_name)
                            table_fields_list.append(field_name_type.lower())

                # check if there are duplicate columns
                if (len(field_types) != len(set(field_types))):
                    status_code = '400'
                    if status_code == '400':
                        errormsgs_val = "There are one or more columns with the same name."
                        errormsgs.append(errormsgs_val)
                        ctx['errormsgs'] = errormsgs
                        return render_to_response(template, RequestContext(request, {'form_csv_layer': form_csv_layer, 'form_empty_layer': form_empty_layer, 'countries': countries, 'errormsgs': errormsgs, 'status_msg': json.dumps('400_empty_layer'), "is_layer": True}))

                geom = "the_geom geometry(%s,4326)" % table_geom
                table_fields_list.append(geom)
                primary_key = "CONSTRAINT %s_pkey PRIMARY KEY (fid)" % table_name
                table_fields_list.append(primary_key)
                table_fields_list = ','.join(map(str, table_fields_list))

                # create table in postgis for empty_layer
                errormsgs_val, status_code = create_empty_layer(table_name, table_fields_list)

                if status_code == '400':
                    errormsgs.append(errormsgs_val)
                    ctx['errormsgs'] = errormsgs
                    return render_to_response(template, RequestContext(request, {'form_csv_layer': form_csv_layer, 'form_empty_layer': form_empty_layer, 'countries': countries, 'errormsgs': errormsgs, 'status_msg': json.dumps('400_empty_layer'), "is_layer": True}))


                available_sld_styles = {
                    'POINT': 'point_style.sld',
                    'MULTILINESTRING': 'line_style.sld',
                    'MULTIPOLYGON': 'polygon_style.sld',
                }
                sld_style = available_sld_styles[table_geom]
                # create geoserver and geonode layer
                _create_geoserver_geonode_layer(table_name, sld_style, title, the_user, permissions)

                ctx['success'] = True
                if ctx['success']:
                    status_code = 200
                    layer = 'geonode:' + table_name

                    return HttpResponseRedirect(
                        reverse(
                            'layer_metadata',
                            args=(
                                layer,
                            )))
            else:
                for e in form_empty_layer.errors.values():
                    errormsgs.append([escape(v) for v in e])

                ctx['errors'] = form_csv_layer.errors
                ctx['errormsgs'] = errormsgs
                ctx['success'] = False
                return render_to_response(template, RequestContext(request, {'form_csv_layer': form_csv_layer, 'form_empty_layer': form_empty_layer, 'countries': countries, 'status_msg': json.dumps('400_empty_layer'), "is_layer": True}))



def _create_geoserver_geonode_layer(new_table, sld_type, title, the_user, permissions):
    # Create the Layer in GeoServer from the table
    try:
        cat = Catalog(settings.OGC_SERVER['default']['LOCATION'] + "rest", settings.OGC_SERVER['default']['USER'], settings.OGC_SERVER['default']['PASSWORD'])
        ds = cat.get_store("uploaded")  # name of store in WFP-Geonode
        cat.publish_featuretype(new_table, ds, "EPSG:4326", srs="EPSG:4326")

        # changing the layer's title in the title set by the user
        resource = cat.get_resource(new_table, workspace="geonode")
        resource.title = title
        cat.save(resource)

    except Exception as e:

        msg = "Error creating GeoServer layer for %s: %s" % (new_table, str(e))
        print msg
        return None, msg

    # Create the Layer in GeoNode from the GeoServer Layer
    try:

        link_to_sld = "{location}styles/{sld_type}".format(** {
            'location': settings.OGC_SERVER['default']['LOCATION'],
            'sld_type': sld_type
        })

        r = requests.get(link_to_sld)
        sld = r.text
        sld = sld.replace("name_of_layer", new_table)  # "name_of_layer" is set in the predefined sld in geoserver (polygon_style, line_style, point_style)
        cat.create_style(new_table, sld, overwrite=True)
        style = cat.get_style(new_table)
        layer = cat.get_layer(new_table)
        layer.default_style = style
        cat.save(layer)
        gs_slurp(owner=the_user, filter=new_table)

        from geonode.base.models import ResourceBase
        layer = ResourceBase.objects.get(title=title)
        geoserver_post_save(layer, ResourceBase)

        # assign permissions for this layer
        permissions_dict = json.loads(permissions)  # needs to be dictionary
        if permissions_dict is not None and len(permissions_dict.keys()) > 0:
            layer.set_permissions(permissions_dict)


    except Exception as e:
        msg = "Error creating GeoNode layer for %s: %s" % (new_table, str(e))
        return None, msg


@login_required
def download_csv(request):

    if request.method == 'GET':
        corresponding_data = {
            "country": {
                "columns": "adm0_code,adm0_name",
                "table_name": "wld_bnd_adm0_gaul_2015"
            },
            "region": {
                "columns": "adm1_code,adm1_name",
                "table_name": "wld_bnd_adm1_gaul_2015",
                "column_1": "adm0_name"
            },
            "province": {
                "columns": "adm2_code,adm2_name",
                "table_name": "wld_bnd_adm2_gaul_2015",
                "column_1": "adm0_name"
            }
        }
        country = request.GET.get('country')
        btn = request.GET.get('btn')

        constr = "dbname='{dbname}' user='{user}' host='{host}' password='{password}'".format(** {
            'dbname': settings.DATABASES['uploaded']['NAME'],
            'user': settings.DATABASES['uploaded']['USER'],
            'host': settings.DATABASES['uploaded']['HOST'],
            'password': settings.DATABASES['uploaded']['PASSWORD']
        })

        conn = psycopg2.connect(constr)
        cur = conn.cursor()

        if (btn == "country"):
            sqlstr = "SELECT {columns} FROM {table} ORDER BY 2".format(** {
                'columns': corresponding_data[btn]["columns"],
                'table': corresponding_data[btn]["table_name"]
            })
        else:
            sqlstr = "SELECT {columns} FROM {table} WHERE {column_1} = '{country}' ORDER BY 2".format(** {
                'columns': corresponding_data[btn]["columns"],
                'country': country,
                'table': corresponding_data[btn]["table_name"],
                'column_1': corresponding_data[btn]["column_1"],
            })

        cur.execute(sqlstr)
        rows = cur.fetchall()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = "attachment; filename={file}".format(** {
            'file': corresponding_data[btn]["table_name"] + ".csv"
        })

        writer = csv.writer(response, dialect='excel')
        writer.writerow(tuple(corresponding_data[btn]["columns"].split(',')))

        for row in rows:
            field_1 = row[0]
            field_2 = unidecode(row[1]).encode(encoding='UTF-8')
            fields = [field_1, field_2]
            writer.writerows([fields])
        return response
