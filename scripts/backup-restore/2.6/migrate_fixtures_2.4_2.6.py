# -*- coding: utf-8 -*-

import json
from shutil import copyfile

source_dir = 'fixtures_backup'
dest_dir = 'fixtures_migrated'

#############################################################
# groups
#############################################################
# no changes, just copying
file_name='groups.json'
copyfile(source_dir+'/'+file_name, dest_dir+'/'+file_name)

#############################################################
# people
#############################################################
# only last_login column switched to nullable: just copying
file_name='people.json'
copyfile(source_dir+'/'+file_name, dest_dir+'/'+file_name)

#############################################################
# accounts
#############################################################
# no changes, just copying
file_name='accounts.json'
copyfile(source_dir+'/'+file_name, dest_dir+'/'+file_name)

#############################################################
# avatars
#############################################################
# no changes, just copying
file_name='avatars.json'
copyfile(source_dir+'/'+file_name, dest_dir+'/'+file_name)

#############################################################
# backups
#############################################################
# The table was missing in 2.4, skipping

#############################################################
# licenses
#############################################################
# no changes, just copying
# TODO: Loaded from initial_data fixture
file_name='licenses.json'
copyfile(source_dir+'/'+file_name, dest_dir+'/'+file_name)

#############################################################
# topiccategories
#############################################################
# fa_class column added (not null)
# TODO: Loaded from initial_data fixture
file_name='topiccategories.json'
with open(source_dir+'/'+file_name, 'r') as f:
    default_obj = json.load(f)

for obj in default_obj:
    obj['fields']['fa_class'] = ''

with open(dest_dir+'/'+file_name, 'w') as w:
    json.dump(default_obj, w)

#############################################################
# regions
#############################################################
# no changes, just copying
# TODO: Loaded from initial_data fixture
file_name='regions.json'
copyfile(source_dir+'/'+file_name, dest_dir+'/'+file_name)

#############################################################
# resourcebases
#############################################################
# Removed:
#  distribution_url               | text                     | 
#  distribution_description       | text                     | 
# Added:
#  metadata_uploaded_preserve     | boolean                  | not null
file_name='resourcebases.json'
with open(source_dir+'/'+file_name, 'r') as f:
    default_obj = json.load(f)

for obj in default_obj:

    try:
        obj['fields'].pop("distribution_description", None)
    except:
        pass

    try:
        obj['fields'].pop("distribution_url", None)
    except:
        pass

    obj['fields']['metadata_uploaded_preserve'] = False

with open(dest_dir+'/'+file_name, 'w') as w:
    json.dump(default_obj, w)

#############################################################
# contactroles
#############################################################
# only resource_id column switched to nullable, just copying
file_name='contactroles.json'
copyfile(source_dir+'/'+file_name, dest_dir+'/'+file_name)

#############################################################
# links
#############################################################
# only resource_id column switched to nullable, just copying
file_name='links.json'
copyfile(source_dir+'/'+file_name, dest_dir+'/'+file_name)

#############################################################
# restrictioncodetypes
#############################################################
# no changes, just copying
# TODO: Loaded from initial_data fixture
file_name='restrictioncodetypes.json'
copyfile(source_dir+'/'+file_name, dest_dir+'/'+file_name)

#############################################################
# spatialrepresentationtypes
#############################################################
# no changes, just copying
# TODO: Loaded from initial_data fixture
file_name='spatialrepresentationtypes.json'
copyfile(source_dir+'/'+file_name, dest_dir+'/'+file_name)

#############################################################
# useropermissions
#############################################################
# no changes, just copying
file_name='useropermissions.json'
copyfile(source_dir+'/'+file_name, dest_dir+'/'+file_name)

#############################################################
# groupopermissions
#############################################################
# no changes, just copying
file_name='groupopermissions.json'
copyfile(source_dir+'/'+file_name, dest_dir+'/'+file_name)

#############################################################
# uploadsessions
#############################################################
# no changes, just copying
file_name='uploadsessions.json'
copyfile(source_dir+'/'+file_name, dest_dir+'/'+file_name)

#############################################################
# styles
#############################################################
# no changes, just copying
file_name='styles.json'
copyfile(source_dir+'/'+file_name, dest_dir+'/'+file_name)

#############################################################
# layers
#############################################################
# Removed:
#  distribution_description_en | text                   | 
# Added:
#  is_mosaic                   | boolean                | not null
#  has_time                    | boolean                | not null
#  has_elevation               | boolean                | not null
#  time_regex                  | character varying(128) | 
#  elevation_regex             | character varying(128) | 
file_name='layers.json'
with open(source_dir+'/'+file_name, 'r') as f:
    default_obj = json.load(f)

for obj in default_obj:

    try:
        obj['fields'].pop("distribution_description_en", None)
    except:
        pass

    try:
        obj['fields'].pop("service", None)
    except:
        pass

    obj['fields']['is_mosaic'] = False
    obj['fields']['has_time'] = False
    obj['fields']['has_elevation'] = False

with open(dest_dir+'/'+file_name, 'w') as w:
    json.dump(default_obj, w)

#############################################################
# attributes
#############################################################
# no changes, just copying
file_name='attributes.json'
copyfile(source_dir+'/'+file_name, dest_dir+'/'+file_name)

#############################################################
# layerfiles
#############################################################
# no changes, just copying
file_name='layerfiles.json'
copyfile(source_dir+'/'+file_name, dest_dir+'/'+file_name)

#############################################################
# maps
#############################################################
# Removed:
#  distribution_description_en | text                   | 
file_name='maps.json'
with open(source_dir+'/'+file_name, 'r') as f:
    default_obj = json.load(f)

for obj in default_obj:

    try:
        obj['fields'].pop("distribution_description_en", None)
    except:
        pass

with open(dest_dir+'/'+file_name, 'w') as w:
    json.dump(default_obj, w)

#############################################################
# maplayers
#############################################################
# no changes, just copying
file_name='maplayers.json'
copyfile(source_dir+'/'+file_name, dest_dir+'/'+file_name)

#############################################################
# mapsnapshots
#############################################################
# no changes, just copying
file_name='mapsnapshots.json'
copyfile(source_dir+'/'+file_name, dest_dir+'/'+file_name)

#############################################################
# documents
#############################################################
# Removed:
#  distribution_description_en | text                   | 
file_name='documents.json'
with open(source_dir+'/'+file_name, 'r') as f:
    default_obj = json.load(f)

for obj in default_obj:

    try:
        obj['fields'].pop("distribution_description_en", None)
    except:
        pass

with open(dest_dir+'/'+file_name, 'w') as w:
    json.dump(default_obj, w)

#############################################################
# tags
#############################################################
# no changes, just copying
file_name='tags.json'
copyfile(source_dir+'/'+file_name, dest_dir+'/'+file_name)
