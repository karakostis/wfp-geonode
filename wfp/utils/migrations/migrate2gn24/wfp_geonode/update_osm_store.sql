update layers_layer
set store = 'osm' where typename in (
'geonode:npl_pop_builduse_osm',
'geonode:npl_poi_healthfacilities_osm', 
'geonode:npl_poi_educationfacilities_osm',
'geonode:npl_trs_roads_osm',
'geonode:npl_phy_landuse_osm'
);
