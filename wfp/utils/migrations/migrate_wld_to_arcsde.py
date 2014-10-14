from geoserver.catalog import Catalog
from django.conf import settings
    
layers_to_process = (
'wld_trs_stations_wfp',
'wld_poi_facilities_wfp',
'wld_poi_warehouses_wfp',
'wld_trs_supplyroutes_wfp',
'wld_trs_unhasroutes_wfp',
'wld_trs_airports_wfp',
'wld_trs_ports_wfp',
'wld_poi_bcp_wfp',
'wld_trs_obstacles_wfp',
'wld_trs_bridges_wfp',
'wld_trs_railways_wfp',
)

def rename_layers_old_postfix():
    """ Rename the layers adding an _old suffix.
    """
    # fixme it does not work, as name cannot be assigned with gsconfig
    # filing a bug
    cat = Catalog("%srest" % settings.GEOSERVER_URL)
    for l in layers_to_process:
        print 'Renaming layer %s' % l
        layer = cat.get_layer(l)
        layer.name = '%s_old' % l
        cat.save(layer)
        cat.reload()
    
def styles2sde_using_gsconfig():
    """ Migrate the layers styles from postgis to sde using gsconfig.
    """
    #geoserver_url = settings.GEOSERVER_URL # http://localhost:8080/geoserver/
    geoserver_url = 'http://geonode.wfp.org/geoserver/'
    user = settings.OGC_SERVER['default']['USER']
    pwd = settings.OGC_SERVER['default']['PASSWORD']
    cat = Catalog("%srest" % geoserver_url, "admin", "zeeD4ies")
    for l in layers_to_process:
        print 'Processing layer %s' % l
        layer_old = cat.get_layer('%s_old' % l)
        layer = cat.get_layer(l)
        #import ipdb;ipdb.set_trace()
        print 'Copying stuff from %s to %s...' % (layer_old.name, layer.name)
        print 'Default style: %s' % layer_old.default_style
        # change default style
        layer.default_style = layer_old.default_style
        # associate styles
        layer.styles = layer_old.styles
        cat.save(layer)
        cat.reload()
        print 'You need to run updatelayers now!'

def styles2sde_using_django():
    """ Migrate the layers styles from postgis to sde using django.
    """
    # this approach do the migration to the arcsde layers using django
    # unluckily this approach does not work as when saving the layers
    # the info are synced back from geoserver and lost in django
    from geonode.layers.models import Layer
    for l in layers_to_process:
        layer = Layer.objects.filter(name=l)[0]
        layer_old = Layer.objects.filter(name='%s_old' % l)[0]
        print 'Copying stuff from %s to %s...' % (layer_old.name, layer.name)
        print 'Default style: %s' % layer_old.default_style
        # change default style
        layer.default_style = layer.default_style
        layer.save()
        # import ipdb;ipdb.set_trace()
        for style in layer_old.styles.all():
            print 'Adding %s style...' % style.name
            layer.styles.add(style)

