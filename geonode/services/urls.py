#########################################################################
#
# Copyright (C) 2017 OSGeo
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

from django.urls import re_path

from . import views

urlpatterns = [
    # 'geonode.services.views',
    re_path(r"^$", views.services, name="services"),
    re_path(r"^register/$", views.register_service, name="register_service"),
    re_path(r"^(?P<service_id>\d+)/$", views.service_detail, name="service_detail"),
    re_path(r"^(?P<service_id>\d+)/edit$", views.edit_service, name="edit_service"),
    re_path(r"^(?P<service_id>\d+)/rescan$", views.rescan_service, name="rescan_service"),
    re_path(r"^(?P<service_id>\d+)/remove", views.remove_service, name="remove_service"),
    re_path(r"^(?P<service_id>\d+)/harvest$", views.harvest_resources, name="harvest_resources"),
    re_path(
        r"^(?P<service_id>\d+)/harvest/(?P<resource_id>\S+)",
        views.harvest_single_resource,
        name="harvest_single_resource",
    ),
]
