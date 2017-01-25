# -*- coding: utf-8 -*-

import os, sys

apps = ["auth_group", "people", "account", "avatar_avatar", "base_resourcebase", "base_contactrole", "base_link", "guardian_userobjectpermission", "guardian_groupobjectpermission", "layers_uploadsession", "layers_style", "layers_layer", "layers_attribute", "layers_layerfile", "maps_map", "maps_maplayer", "maps_mapsnapshot", "documents_document", "taggit"]

dumps = ["groups", "people", "accounts", "avatars", "resourcebases", "contactroles", "links", "useropermissions", "groupopermissions", "uploadsessions", "styles", "layers", "attributes", "layerfiles", "maps", "maplayers", "mapsnapshots", "documents", "tags"]

fixtures_path = "~/fixtures_migrated"

for app_name, dump_name in zip(apps, dumps):
  print "Loading fixture '"+dump_name+".json' into '"+app_name+"' database table."
  os.system("python manage.py loaddata %s/%s.json %s" % (fixtures_path, dump_name, app_name))

