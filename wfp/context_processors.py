from wfp import get_version


def wfp_geonode(request):
    """ Global values related to WFPGeoNode to pass to templates """

    return dict(
        WFPGEONODE_VERSION=get_version(),
    )
