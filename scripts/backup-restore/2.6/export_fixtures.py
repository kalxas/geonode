# -*- coding: utf-8 -*-

import os, sys

apps = ["auth.group", "people", "account", "avatar.avatar", "base.backup", "base.license", "base.topiccategory", "base.region", "base.resourcebase", "base.contactrole", "base.link", "base.restrictioncodetype", "base.spatialrepresentationtype", "guardian.userobjectpermission", "guardian.groupobjectpermission", "layers.uploadsession", "layers.style", "layers.layer", "layers.attribute", "layers.layerfile", "maps.map", "maps.maplayer", "maps.mapsnapshot", "documents.document", "taggit"]

dumps = ["groups", "people", "accounts", "avatars", "backups", "licenses", "topiccategories", "regions", "resourcebases", "contactroles", "links", "restrictioncodetypes", "spatialrepresentationtypes", "useropermissions", "groupopermissions", "uploadsessions", "styles", "layers", "attributes", "layerfiles", "maps", "maplayers", "mapsnapshots", "documents", "tags"]

for app_name, dump_name in zip(apps, dumps):
  print "Dumping '"+app_name+"' into '"+dump_name+".json'."
  os.system("django-admin.py dumpdata %s --format=json > %s.json" % (app_name, dump_name))

