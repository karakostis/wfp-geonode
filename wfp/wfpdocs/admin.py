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

from django.contrib import admin
from wfp.wfpdocs.models import WFPDocument, Category


class WFPDocumentAdmin(admin.ModelAdmin):
    """
    Admin for a static map.
    """
    list_display = ('title', 'date', 'date_updated', 'get_layers',
                    'get_regions', 'source', 'get_categories', 'orientation', 'page_format',
                    'extension',)
    list_display_links = ('title',)
    list_filter = ('orientation', 'page_format', 'categories', 'extension', 'regions',)
    search_fields = ('title',)
    date_hierarchy = 'date'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )


admin.site.register(WFPDocument, WFPDocumentAdmin)
admin.site.register(Category, CategoryAdmin)
