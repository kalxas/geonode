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

# based on https://github.com/geopython/pycsw/blob/master/pycsw/core/config.py
MD_CORE_MODEL = {
    "typename": "pycsw:CoreMetadata",
    "outputschema": "http://pycsw.org/metadata",
    "mappings": {
        "pycsw:Identifier": "uuid",
        "pycsw:Typename": "csw_typename",
        "pycsw:Schema": "csw_schema",
        "pycsw:MdSource": "csw_mdsource",
        "pycsw:InsertDate": "csw_insert_date",
        "pycsw:XML": "metadata_xml",
        "pycsw:Metadata": "metadata",
        "pycsw:MetadataType": "metadata_type",
        "pycsw:AnyText": "csw_anytext",
        "pycsw:Language": "language",
        "pycsw:Title": "title",
        "pycsw:Abstract": "raw_abstract",
        "pycsw:Edition": "edition",
        "pycsw:Keywords": "keyword_csv",
        "pycsw:KeywordType": "keywordstype",
        "pycsw:Themes": "csw_themes",
        "pycsw:Format": "spatial_representation_type_string",
        "pycsw:Source": "source",
        "pycsw:Date": "date",
        "pycsw:Modified": "date",
        "pycsw:Type": "csw_type",
        "pycsw:BoundingBox": "csw_wkt_geometry",
        "pycsw:VertExtentMin": "csw_vert_extent_min",
        "pycsw:VertExtentMax": "csw_vert_extent_max",
        "pycsw:CRS": "csw_crs",
        "pycsw:AlternateTitle": "alternate",
        "pycsw:RevisionDate": "date",
        "pycsw:CreationDate": "date",
        "pycsw:PublicationDate": "date",
        "pycsw:OrganizationName": "organizationname",
        "pycsw:SecurityConstraints": "securityconstraints",
        "pycsw:ParentIdentifier": "parentidentifier",
        "pycsw:TopicCategory": "topiccategory",
        "pycsw:ResourceLanguage": "language",
        "pycsw:GeographicDescriptionCode": "geodescode",
        "pycsw:Denominator": "denominator",
        "pycsw:DistanceValue": "distancevalue",
        "pycsw:DistanceUOM": "distanceuom",
        "pycsw:TempExtent_begin": "temporal_extent_start",
        "pycsw:TempExtent_end": "temporal_extent_end",
        "pycsw:ServiceType": "servicetype",
        "pycsw:ServiceTypeVersion": "servicetypeversion",
        "pycsw:Operation": "operation",
        "pycsw:CouplingType": "couplingtype",
        "pycsw:OperatesOn": "operateson",
        "pycsw:OperatesOnIdentifier": "operatesonidentifier",
        "pycsw:OperatesOnName": "operatesoname",
        "pycsw:Degree": "degree",
        "pycsw:AccessConstraints": "restriction_code",
        "pycsw:OtherConstraints": "raw_constraints_other",
        "pycsw:Classification": "classification",
        "pycsw:ConditionApplyingToAccessAndUse": "conditionapplyingtoaccessanduse",
        "pycsw:Lineage": "lineage",
        "pycsw:ResponsiblePartyRole": "responsiblepartyrole",
        "pycsw:SpecificationTitle": "specificationtitle",
        "pycsw:SpecificationDate": "specificationdate",
        "pycsw:SpecificationDateType": "specificationdatetype",
        "pycsw:Creator": "creator",
        "pycsw:Publisher": "publisher",
        "pycsw:Contributor": "contributor",
        "pycsw:Relation": "relation",
        "pycsw:Platform": "platform",
        "pycsw:Instrument": "instrument",
        "pycsw:SensorType": "sensortype",
        "pycsw:CloudCover": "cloudcover",
        "pycsw:Bands": "bands",
        "pycsw:Links": "download_links",
        "pycsw:Contacts": "contacts",
    },
}
