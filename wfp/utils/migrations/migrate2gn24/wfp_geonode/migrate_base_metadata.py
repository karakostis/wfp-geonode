#!/usr/bin/python
import os, sys

path = os.path.dirname(__file__)
geonode_path = os.path.abspath(os.path.join(path, '../../../../..'))
sys.path.append(geonode_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wfp.settings.default")

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

def update_regions():
    # WLD becomes GLO (id=1)
    # HOA, SAH goes under AFR (id=10)
    # OMB, OMD, OMC, OMP, OMJ, ODM goes under GLO (id=1), and becomes RMB, RMC...

    from geonode.base.models import Region

    # WLD becomes GLO (id=1)
    glo = Region.objects.filter(code='GLO')[0]
    glo.code = 'GLO'
    glo.save()

    # HOA, SAH goes under AFR (id=10)
    afr = Region.objects.filter(code='AFR')[0]

    hoa = Region(code='HOA', name='Horn of Africa', parent=afr)
    hoa.save()

    sah = Region(code='SAH', name='Sahel Region', parent=afr)
    sah.save()

    # OMB, OMD, OMC, OMP, OMJ, ODM goes under GLO (id=1), and becomes RMB, RMC...
    for rb in ('RBB', 'RBD', 'RBC', 'RBP', 'RBJ', 'RBN'):
        omc = Region(code=rb, name='%s Region' % rb, parent=glo)
        omc.save()

    print 'Model Region migrated'

def update_representationtypes():
    # identifier: grid, gn_description: raster data
    # identifier: textTable, gn_description: document
    # identifier: vector, gn_description: vector data
    # identifier: stereoModel, is_choice: false
    # identifier: tin, is_choice: false
    # identifier: video, is_choice: false
    
    from geonode.base.models import SpatialRepresentationType

    for identifier in ('stereoModel', 'tin', 'video'):
        sr = SpatialRepresentationType.objects.get(identifier=identifier)
        sr.is_choice = False
        sr.save()

    sr = SpatialRepresentationType.objects.get(identifier='grid')
    sr.gn_description = 'raster data'
    sr.save()

    sr = SpatialRepresentationType.objects.get(identifier='textTable')
    sr.gn_description = 'document'
    sr.save()

    sr = SpatialRepresentationType.objects.get(identifier='vector')
    sr.gn_description = 'vector data'
    sr.save()

    print 'Model SpatialRepresentationType migrated'

def update_restrictions():
    # identifier: license, gn_description: No restrictions
    # identifier: limitation not listed, gn_description: Other restrictions
    # identifier: patent, gn_description: Government has granted exclusive right to WFP for internal use
    # identifier: restricted, gn_description: Withheld from general circulation or disclosure
    # identifier: copyright, is_choice: false
    # identifier: intellectualPropertyRights, is_choice: false
    # identifier: patentPending, is_choice: false
    # identifier: trademark, is_choice: false

    from geonode.base.models import RestrictionCodeType

    for identifier in ('copyright', 'intellectualPropertyRights', 'patentPending', 'trademark'):
        rct = RestrictionCodeType.objects.get(identifier=identifier)
        rct.is_choice = False
        rct.save()

    rct = RestrictionCodeType.objects.get(identifier='license')
    rct.gn_description = 'No restrictions'
    rct.save()

    rct = RestrictionCodeType.objects.get(identifier='limitation not listed')
    rct.gn_description = 'Other restrictions'
    rct.save()
    
    rct = RestrictionCodeType.objects.get(identifier='patent')
    rct.gn_description = 'Government has granted exclusive right to WFP for internal use'
    rct.save()
    
    rct = RestrictionCodeType.objects.get(identifier='restricted')
    rct.gn_description = 'Withheld from general circulation or disclosure'
    rct.save()
    
    print 'Model RestrictionCodeType migrated'

def update_topiccategories():
    # identifier: biota, gn_description: Natural Hazards
    # identifier: economy, gn_description: Food Security & Nutrition
    # identifier: farming, gn_description: Markets
    # identifier: geoscientificInformation, gn_description: WFP Locations of Interest
    # identifier: ImageryBaseMapsEarthCover, gn_description: Satellite Imagery & Remote Sensing
    # identifier: inlandWaters, gn_description: Hydrology
    # identifier: intelligenceMilitary, gn_description: Financial
    # identifier: location, gn_description: Points of Interest
    # identifier: oceans, gn_description: Security
    # identifier: planningCadastre, gn_description: WFP Programmes
    # identifier: society, gn_description: Population
    # identifier: structure, gn_description: Others
    # identifier: utilitiesCommunication, gn_description: Utilities

    from geonode.base.models import TopicCategory

    categories = (
        {'identifier': 'biota', 'gn_description': 'Natural Hazards'},
        {'identifier': 'economy', 'gn_description': 'Food Security & Nutrition'},
        {'identifier': 'farming', 'gn_description': 'Markets'},
        {'identifier': 'geoscientificInformation', 'gn_description': 'WFP Locations of Interest'},
        {'identifier': 'imageryBaseMapsEarthCover', 'gn_description': 'Satellite Imagery & Remote Sensing'},
        {'identifier': 'inlandWaters', 'gn_description': 'Hydrology'},
        {'identifier': 'intelligenceMilitary', 'gn_description': 'Financial'},
        {'identifier': 'location', 'gn_description': 'Points of Interest'},
        {'identifier': 'oceans', 'gn_description': 'Security'},
        {'identifier': 'planningCadastre', 'gn_description': 'WFP Programmes'},
        {'identifier': 'society', 'gn_description': 'Population'},
        {'identifier': 'structure', 'gn_description': 'Others'},
        {'identifier': 'utilitiesCommunication', 'gn_description': 'Utilities'},
    )

    for category in categories:
        print category['identifier'], category['gn_description']
        tc = TopicCategory.objects.get(identifier=category['identifier'])
        tc.gn_description = category['gn_description']
        tc.save()

    print 'Model TopicCategory migrated'

update_regions()
update_representationtypes()
update_restrictions()
update_topiccategories()
