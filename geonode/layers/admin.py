#########################################################################
#
# Copyright (C) 2016 OSGeo
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

from modeltranslation.admin import TabbedTranslationAdmin

from geonode.base.admin import ResourceBaseAdminForm, SparseInline
from geonode.layers.models import Dataset, Attribute, Style


class AttributeInline(admin.TabularInline):
    model = Attribute


class DatasetAdminForm(ResourceBaseAdminForm):
    class Meta(ResourceBaseAdminForm.Meta):
        model = Dataset
        fields = "__all__"


class DatasetAdmin(TabbedTranslationAdmin):
    exclude = ("ll_bbox_polygon", "bbox_polygon", "srid", "tkeywords")
    list_display = (
        "id",
        "alternate",
        "title",
        "date",
        "category",
        "group",
        "is_approved",
        "is_published",
        "state",
        "dirty_state",
        "metadata_completeness",
    )
    list_display_links = ("id",)
    list_editable = ("title", "category", "group", "is_approved", "is_published", "dirty_state")
    list_filter = (
        "subtype",
        "owner",
        "category",
        "group",
        "restriction_code_type__identifier",
        "date",
        "date_type",
        "is_approved",
        "is_published",
        "state",
        "dirty_state",
    )
    search_fields = ("alternate", "title", "abstract", "purpose", "is_approved", "is_published", "state")
    filter_horizontal = ("contacts",)
    date_hierarchy = "date"
    readonly_fields = ("uuid", "alternate", "workspace", "geographic_bounding_box")
    inlines = (
        AttributeInline,
        SparseInline,
    )
    form = DatasetAdminForm

    def delete_queryset(self, request, queryset):
        """
        We need to invoke the 'ResourceBase.delete' method even when deleting
        through the admin batch action
        """
        for obj in queryset:
            from geonode.resource.manager import resource_manager

            resource_manager.delete(obj.uuid, instance=obj)


class AttributeAdmin(admin.ModelAdmin):
    model = Attribute
    list_display_links = ("id",)
    list_display = ("id", "dataset", "attribute", "description", "attribute_label", "attribute_type", "display_order")
    list_filter = ("dataset", "attribute_type")
    search_fields = (
        "attribute",
        "attribute_label",
    )


class StyleAdmin(admin.ModelAdmin):
    model = Style
    list_display_links = ("sld_title",)
    list_display = ("id", "name", "sld_title", "workspace", "sld_url")
    list_filter = ("workspace",)
    search_fields = (
        "name",
        "workspace",
    )


admin.site.register(Dataset, DatasetAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Style, StyleAdmin)
