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
import json
import logging

from unittest.mock import patch
from rest_framework import status

from django.urls import reverse
from django.contrib.auth import get_user_model

from geonode import geoserver
from geonode.maps.apps import MapsAppConfig
from geonode.layers.models import Dataset
from geonode.compat import ensure_string
from geonode.decorators import on_ogc_backend
from geonode.maps.models import Map, MapLayer
from geonode.tests.utils import NotificationsTestsHelper
from geonode.maps.tests_populate_maplayers import create_maplayers
from geonode.resource.manager import resource_manager

from geonode.base.populate_test_data import all_public, create_models, remove_models

logger = logging.getLogger(__name__)

VIEWER_CONFIG = """
{
  "defaultSourceType": "gx_wmssource",
  "about": {
      "title": "Title",
      "abstract": "Abstract"
  },
  "sources": {
    "capra": {
      "url":"http://localhost:8080/geoserver/wms"
    }
  },
  "map": {
    "projection":"EPSG:3857",
    "units":"m",
    "maxResolution":156543.0339,
    "maxExtent":[-20037508.34,-20037508.34,20037508.34,20037508.34],
    "center":[-9428760.8688778,1436891.8972581],
    "layers":[{
      "source":"capra",
      "buffer":0,
      "wms":"capra",
      "name":"base:nic_admin"
    }],
    "keywords":["saving", "keywords"],
    "zoom":7
  }
}
"""


class MapsTest(NotificationsTestsHelper):
    """Tests geonode.maps app/module"""

    fixtures = ["initial_data.json", "group_test_data.json", "default_oauth_apps.json"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        create_models(type=cls.get_type, integration=cls.get_integration)
        all_public()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        remove_models(cls.get_obj_ids, type=cls.get_type, integration=cls.get_integration)

    def setUp(self):
        super().setUp()

        self.user = "admin"
        self.passwd = "admin"
        create_maplayers()
        self.not_admin = get_user_model().objects.create(username="r-lukaku", is_active=True)
        self.not_admin.set_password("very-secret")
        self.not_admin.save()

        self.u = get_user_model().objects.get(username=self.user)
        self.u.email = "test@email.com"
        self.u.is_active = True
        self.u.save()
        self.setup_notifications_for(MapsAppConfig.NOTIFICATIONS, self.u)

        self.norman = get_user_model().objects.get(username="norman")
        self.norman.email = "norman@email.com"
        self.norman.is_active = True
        self.norman.save()
        self.setup_notifications_for(MapsAppConfig.NOTIFICATIONS, self.norman)

    default_abstract = "This is a demonstration of GeoNode, an application \
for assembling and publishing web based maps.  After adding layers to the map, \
use the Save Map button above to contribute your map to the GeoNode \
community."

    default_title = "GeoNode Default Map"

    # This is a valid map viewer config, based on the sample data provided
    # by andreas in issue 566. -dwins
    viewer_config = VIEWER_CONFIG

    viewer_config_alternative = """
    {
      "defaultSourceType": "gx_wmssource",
      "about": {
          "title": "Title2",
          "abstract": "Abstract2"
      },
      "sources": {
        "capra": {
          "url":"http://localhost:8080/geoserver/wms"
        }
      },
      "map": {
        "projection":"EPSG:3857",
        "units":"m",
        "maxResolution":156543.0339,
        "maxExtent":[-20037508.34,-20037508.34,20037508.34,20037508.34],
        "center":[-9428760.8688778,1436891.8972581],
        "layers":[{
          "source":"capra",
          "buffer":0,
          "wms":"capra",
          "name":"base:nic_admin"
        }],
        "zoom":7
      }
    }
    """

    perm_spec = {
        "users": {"admin": ["change_resourcebase", "change_resourcebase_permissions", "view_resourcebase"]},
        "groups": {},
    }

    def test_ajax_map_permissions(self):
        """Verify that the ajax_dataset_permissions view is behaving as expected"""

        # Setup some layer names to work with
        mapid = Map.objects.all().first().pk
        invalid_mapid = "42"

        def url(id):
            return reverse("resource_permissions", args=[id])

        # Test that an invalid layer.alternate is handled for properly
        response = self.client.post(
            url(invalid_mapid), data=json.dumps(self.perm_spec), content_type="application/json"
        )
        self.assertNotEqual(response.status_code, 200)

        # Test that GET returns permissions
        response = self.client.get(url(mapid))
        assert "permissions" in ensure_string(response.content)

        # Test that a user is required to have permissions

        # First test un-authenticated
        response = self.client.post(url(mapid), data=json.dumps(self.perm_spec), content_type="application/json")
        self.assertEqual(response.status_code, 401)

        # Next Test with a user that does NOT have the proper perms
        logged_in = self.client.login(username="foo", password="pass")
        self.assertEqual(logged_in, True)
        response = self.client.post(url(mapid), data=json.dumps(self.perm_spec), content_type="application/json")
        self.assertEqual(response.status_code, 401)

        # Login as a user with the proper permission and test the endpoint
        logged_in = self.client.login(username="admin", password="admin")
        self.assertEqual(logged_in, True)

        response = self.client.post(url(mapid), data=json.dumps(self.perm_spec), content_type="application/json")

        # Test that the method returns 200
        self.assertEqual(response.status_code, 200)

    @on_ogc_backend(geoserver.BACKEND_PACKAGE)
    @patch("geonode.thumbs.thumbnails.create_thumbnail")
    def test_map_embed(self, thumbnail_mock):
        """Test that map can be properly embedded"""
        # first create a map
        map_created = Map.objects.create(owner=self.u)
        MapLayer.objects.create(
            map=map_created,
            name="base:nic_admin",
            ows_url="http://localhost:8080/geoserver/wms",
        )
        map_id = map_created.id

        url = reverse("map_embed", args=(map_id,))
        url_no_id = reverse("map_embed")

        # Now test with a map id
        self.client.login(username=self.user, password=self.passwd)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # The embedded map is exempt from X-FRAME-OPTIONS restrictions.
        if hasattr(response, "xframe_options_exempt"):
            self.assertTrue(response.xframe_options_exempt)

        # Config equals to that of the map whose id is given
        map_obj = Map.objects.get(id=map_id)
        self.assertEqual(response.context["resource"], map_obj)
        self.assertIsNotNone(response.context["access_token"])
        self.assertEqual(response.context["is_embed"], "true")

        # Now test without a map id
        response = self.client.get(url_no_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch("geonode.thumbs.thumbnails.create_thumbnail")
    def test_map_view(self, thumbnail_mock):
        """Test that map view can be properly rendered"""
        # first create a map
        map_created = Map.objects.create(owner=self.u)
        MapLayer.objects.create(
            map=map_created,
            name="base:nic_admin",
            ows_url="http://localhost:8080/geoserver/wms",
        )
        resource_manager.set_permissions(None, instance=map_created, permissions=None, created=True)
        map_id = map_created.id

        url = reverse("map_embed", args=(map_id,))

        # test unauthenticated user to view map
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # TODO: unauthenticated user can still access the map view

        # test a user without map view permission
        self.client.login(username="norman", password="norman")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        # TODO: the user can still access the map view without permission

        # Now test with a valid user using GET method
        self.client.login(username=self.user, password=self.passwd)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Config equals to that of the map whose id is given
        map_obj = Map.objects.get(id=map_id)
        map_obj = Map.objects.get(id=map_id)
        self.assertEqual(response.context["resource"], map_obj)
        self.assertIsNotNone(response.context["access_token"])
        self.assertEqual(response.context["is_embed"], "true")

    def test_get_legend(self):
        layer = Dataset.objects.all().first()
        map_dataset = MapLayer.objects.filter(name=layer.alternate).first()
        if map_dataset and layer.default_style:
            self.assertIsNone(map_dataset.get_legend)
        elif map_dataset:
            # when there is no style
            self.assertIsNone(map_dataset.get_legend)

    def test_moderated_upload(self):
        """
        Test if moderation flag works
        """
        with self.settings(ADMIN_MODERATE_UPLOADS=False):
            # first create a map
            map_created = resource_manager.create(None, resource_type=Map, defaults=dict(owner=self.u))
            resource_manager.set_permissions(None, instance=map_created, permissions=None, created=True)
            self.assertTrue(map_created.is_approved)
            self.assertTrue(map_created.is_published)

        with self.settings(ADMIN_MODERATE_UPLOADS=True):
            # first create a map
            map_created = resource_manager.create(None, resource_type=Map, defaults=dict(owner=self.u))
            resource_manager.set_permissions(None, instance=map_created, permissions=None, created=True)
            self.assertFalse(map_created.is_approved)
            self.assertFalse(map_created.is_published)

    def testMapsNotifications(self):
        with self.settings(
            EMAIL_ENABLE=True,
            NOTIFICATION_ENABLED=True,
            NOTIFICATIONS_BACKEND="pinax.notifications.backends.email.EmailBackend",
            PINAX_NOTIFICATIONS_QUEUE_ALL=False,
        ):
            self.clear_notifications_queue()

            # first create a map
            url = reverse("maps-list")

            data = {
                "title": "Some created map",
                "maplayers": [
                    {
                        "name": "base:nic_admin",
                    }
                ],
            }
            self.client.login(username="norman", password="norman")
            response = self.client.post(url, data=json.dumps(data), content_type="application/json")
            self.assertEqual(response.status_code, 201)

            map_id = int(response.data["map"]["pk"])
            _l = Map.objects.get(id=map_id)

            self.assertTrue(self.check_notification_out("map_created", self.u))

            self.clear_notifications_queue()
            _l.title = "test notifications 2"
            _l.save(notify=True)
            self.assertTrue(self.check_notification_out("map_updated", self.u))

            self.clear_notifications_queue()
