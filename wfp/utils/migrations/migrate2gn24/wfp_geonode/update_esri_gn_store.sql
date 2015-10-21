update layers_layer
set store = 'esri_gn' where typename in ('geonode:wld_bnd_presence_wfp', 'geonode:wld_trs_ports_wfp', 'geonode:wld_trs_bridges_wfp', 'geonode:wld_trs_airports_wfp', 
'geonode:wld_trs_unhasroutes_wfp', 'geonode:wld_poi_bcp_wfp', 'geonode:wld_trs_obstacles_wfp', 'geonode:wld_poi_facilities_wfp', 'geonode:wld_trs_stations_wfp', 'geonode:wld_trs_supplyroutes_wfp', 
'geonode:wld_trs_railways_wfp', 'geonode:wld_poi_warehouses_wfp')
