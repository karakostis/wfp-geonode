#!/usr/bin/env python
#########################################################################
#
# Copyright (C) 2012-2015 Paolo Corti, pcorti@gmail.com
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
import json

from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms import HiddenInput

from bootstrap3_datetime.widgets import DateTimePicker
from modeltranslation.forms import TranslationModelForm
import autocomplete_light
from autocomplete_light.contrib.taggit_field import TaggitField, TaggitWidget

from models import WFPDocument

autocomplete_light.autodiscover() # flake8: noqa


class WFPDocumentForm(TranslationModelForm):
    """
    For to upload Static Maps.
    """
    permissions = forms.CharField(
        widget=HiddenInput(
            attrs={
                'name': 'permissions',
                'id': 'permissions'}),
        required=True)
    _date_widget_options = {
        "icon_attrs": {"class": "fa fa-calendar"},
        "attrs": {"class": "form-control input-sm"},
        "format": "%Y-%m-%d %H:%M",
        # Options for the datetimepickers are not set here on purpose.
        # They are set in the metadata_form_js.html template because
        # bootstrap-datetimepicker uses jquery for its initialization
        # and we need to ensure it is available before trying to
        # instantiate a new datetimepicker. This could probably be improved.
        "options": False,
        }
    date = forms.DateTimeField(
        localize=True,
        widget=DateTimePicker(**_date_widget_options)
    )
    keywords = TaggitField(
        required=False,
        help_text=_("A space or comma-separated list of keywords"),
        widget=TaggitWidget('TagAutocomplete'))

    def __init__(self, *args, **kwargs):
        super(WFPDocumentForm, self).__init__(*args, **kwargs)
        # we need to override help_text for title (comes from ResourceBase)
        title_help_text = _(
            'Please use the following convention: Country Name, Theme, Date - '
            'ex: Afghanistan, Snow Forecast, 17 - 23 February 2015'
        )
        title_field = self.fields['title']
        title_field.help_text = title_help_text
        for field in self.fields:
            help_text = self.fields[field].help_text
            self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update(
                    {
                        'class': 'has-popover',
                        'data-content': help_text,
                        'data-placement': 'right',
                        'data-container': 'body',
                        'data-html': 'true'})

    class Meta:
        model = WFPDocument
        fields = (
            'title', 'doc_file', 'source', 'orientation', 'page_format', 'categories',
            'keywords', 'regions', 'last_version', 'layers', 'date',
        )

    def clean_doc_file(self):
        """
        Ensures the doc_file is valid.
        """
        doc_file = self.cleaned_data.get('doc_file')

        if doc_file and not os.path.splitext(
                doc_file.name)[1].lower()[
                1:] in ('gif', 'jpg', 'jpeg', 'pdf', 'png'):
            raise forms.ValidationError(_("This file type is not allowed"))

        return doc_file

    def clean_permissions(self):
        """
        Ensures the JSON field is JSON.
        """
        permissions = self.cleaned_data['permissions']

        try:
            return json.loads(permissions)
        except ValueError:
            raise forms.ValidationError(_("Permissions must be valid JSON."))
