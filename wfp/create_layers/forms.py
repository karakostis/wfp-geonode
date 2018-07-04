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
import tempfile
import zipfile
import psycopg2
import autocomplete_light

from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson as json
from geonode.layers.utils import unzip_file
from geonode.layers.models import Layer, Attribute

autocomplete_light.autodiscover() # flake8: noqa

from geonode.base.forms import ResourceBaseForm

def get_country_names():

    constr = "dbname='{dbname}' user='{user}' host='{host}' password='{password}'".format(** {
        'dbname': settings.DATABASES['uploaded']['NAME'],
        'user': settings.DATABASES['uploaded']['USER'],
        'host': settings.DATABASES['uploaded']['HOST'],
        'password': settings.DATABASES['uploaded']['PASSWORD']
    })

    conn = psycopg2.connect(constr)
    cur = conn.cursor()

    sqlstr = "SELECT DISTINCT ({country_names}) FROM {table} ORDER BY {country_names};".format(** {
        'country_names': 'adm0_name',
        'table': 'wld_bnd_adm0_gaul_2015'
    })

    cur.execute(sqlstr)
    countries = cur.fetchall()
    choices_list = []
    cntr = ['World','World']
    choices_list.append(cntr)
    for i in range(len(countries)):

        cntr = [countries[i][0],countries[i][0]]
        choices_list.append(cntr)

    return choices_list

class UploadCSVForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(UploadCSVForm, self).__init__(*args, **kwargs)
        self.fields['selected_country'] = forms.MultipleChoiceField(choices=get_country_names(), required=True)

    title = forms.CharField(max_length=80, required=True)

    LAYER_TYPE = (
        ('1', 'Global Layer'),
        ('2', 'Layer by Region'),
        ('3', 'Layer by Province'),
    )
    layer_type = forms.ChoiceField(choices=LAYER_TYPE, required=True)
    csv = forms.FileField(required=True)
    permissions_json = forms.CharField(max_length=500, widget=forms.HiddenInput()) #  stores the permissions json from the permissions form


    def write_files(self):
        absolute_base_file = None
        tempdir = tempfile.mkdtemp()
        f = self.cleaned_data['csv']
        if f is not None:
            path = os.path.join(tempdir, f.name)
            with open(path, 'wb') as writable:
                for c in f.chunks():
                    writable.write(c)
        absolute_base_file = os.path.join(tempdir,self.cleaned_data["csv"].name)
        return tempdir, absolute_base_file


    def clean(self):
        cleaned_data = super(UploadCSVForm, self).clean()
        csv_file = self.cleaned_data.get('csv')
        if not csv_file:
            raise forms.ValidationError(_("Please select a CSV file."))
        else:
            csv_file_type = str(csv_file).split('.')
            if csv_file_type[1] not in ['csv','CSV']:
                raise forms.ValidationError(_("This is not a supported format. Please upload a CSV file."))
        return cleaned_data


class UploadEmptyLayerForm(forms.Form):

    empty_layer_name = forms.CharField(max_length=80, required=True, label="Name of new Layer")

    GEOM_TYPE = (
        ('POINT', 'Points'),
        ('MULTILINESTRING', 'Lines'),
        ('MULTIPOLYGON', 'Polygons')
    )

    geom_type = forms.ChoiceField(choices=GEOM_TYPE, required=True, label="Type of Data")
    total_input_fields = forms.CharField(widget=forms.HiddenInput())
    permissions_json = forms.CharField(max_length=500, widget=forms.HiddenInput()) #  stores the permissions json from the permissions form

    def __init__(self, *args, **kwargs):

        FIELD_TYPE = (
            ('Integer', 'Integer'),
            ('Double', 'Double'),
            ('Character', 'Character')
        )

        extra_fields = kwargs.pop('extra', 0)

        if not extra_fields:
            extra_fields = 0

        super(UploadEmptyLayerForm, self).__init__(*args, **kwargs)
        self.fields['total_input_fields'].initial = extra_fields

        for index in range(int(extra_fields)):
            # generate extra fields in the number specified via extra_fields
            self.fields['extra_field_{index}'.format(index=index)] = forms.CharField(min_length=3, max_length=15, label="Attribute %s" % index)
            self.fields['field_type_{index}'.format(index=index)] = forms.ChoiceField(choices=FIELD_TYPE, label="")
