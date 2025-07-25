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

from django.urls import include, re_path

from . import views

js_info_dict = {
    "packages": ("geonode.maps",),
}

map_embed = views.map_embed

urlpatterns = [
    # 'geonode.maps.views',
    re_path(r"^(?P<mapid>[^/]+)/embed$", map_embed, name="map_embed"),
    re_path(r"^embed/$", views.map_embed, name="map_embed"),
    re_path(r"^", include("geonode.maps.api.urls")),
]
