# ##############################################################################
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
# ##############################################################################

from geonode import geoserver  # noqa
from geonode.utils import check_ogc_backend
from django.urls import include, re_path

from . import views

js_info_dict = {
    "packages": ("geonode.layers",),
}

urlpatterns = [
    # 'geonode.layers.views',
    re_path(r"^(?P<layername>[^/]+)/embed$", views.dataset_embed, name="dataset_embed"),
    re_path(
        r"^(?P<layername>[^/]*)/feature_catalogue$", views.dataset_feature_catalogue, name="dataset_feature_catalogue"
    ),
    re_path(r"^(?P<layername>[^/]*)/dataset_download$", views.dataset_download, name="dataset_download"),
    re_path(r"^", include("geonode.layers.api.urls")),
]

# -- Deprecated url routes for Geoserver authentication -- remove after GeoNode 2.1
# -- Use /gs/acls, gs/resolve_user/, gs/download instead
if check_ogc_backend(geoserver.BACKEND_PACKAGE):
    from geonode.geoserver.views import dataset_acls, resolve_user

    urlpatterns = [  # 'geonode.geoserver.views',
        re_path(r"^acls/?$", dataset_acls, name="dataset_acls_dep"),
        re_path(r"^resolve_user/?$", resolve_user, name="dataset_resolve_user_dep"),
    ] + urlpatterns
