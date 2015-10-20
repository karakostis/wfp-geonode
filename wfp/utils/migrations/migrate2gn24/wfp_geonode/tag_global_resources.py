#!/usr/bin/python
import os, sys

path = os.path.dirname(__file__)
geonode_path = os.path.abspath(os.path.join(path, '../../../../..'))
sys.path.append(geonode_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wfp.settings.default")

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from geonode.base.models import ResourceBase
from geonode.base.models import Region

# tagging resources as "global" failed in the migrations, so we do it with this script

uuids = ("b9ff5500-ea3f-11e3-a753-00259028b818",
"0b2400ca-efae-11e3-aa8f-00259028b818",
"e8912bcc-efe0-11e3-9abc-00259028b818",
"6abbcc6c-f06b-11e3-bdd0-00259028b818",
"d535585e-8f38-11e3-a6d1-00259028b818",
"3e63517e-e267-11e3-9edb-00259028b818",
"7fc21a89-7455-4606-9e2a-89c0e0dc46bb",
"8b2bd34b-fc51-4883-9ed1-c22b63f3f944",
"7e657ee3-803b-446a-89cc-5fe045e8428c",
"0d9abe87-29de-425d-9b07-de9d813204d4",
"075fc05f-35b6-4e93-adad-8d828f9c01f5",
"46d34b99-2b55-4d6b-956d-ce2a84a63d9a",
"19e190b0-9b59-4c66-862b-3e8d1c074b40",
"bee5b684-479a-467b-96b6-dcdcb30059a4",
"67a68df2-2a9c-4f22-a6ea-f9fdd7f15cdd",
"c9eee302-87cf-46fa-b673-ccd3f41921eb",
"ecd87644-fce2-4985-bb97-e99a9848cfbe",
"f651ee02-8769-11e3-8927-00259028b818",
"fedac948-1209-11e3-8461-00259028b818",
"bb6c2066-81b8-11e3-9571-00259028b818",
"21ea2201-1e70-488e-b83a-242b80ed845b",
"b346f478-a48c-11e3-a59e-00259028b818",
"1b876e66-c187-11e3-b4de-00259028b818",
"550f88da-dcc1-11e3-b7bc-00259028b818",
"61a8add2-e267-11e3-8475-00259028b818",
"473981b0-e267-11e3-8475-00259028b818",
"c4d9b786-0669-11e4-add7-00259028b818",
"d5d5c85e-13fc-11e4-a826-00259028b818",
"b66a29cc-a48c-11e3-8638-00259028b818",
"86f2fd12-f17c-11e3-855d-00259028b818",
"74f41034-e267-11e3-8475-00259028b818",
"6b16f6e4-e267-11e3-a5e8-00259028b818",
"58c75664-e267-11e3-9edb-00259028b818",
"4fd78dd0-e267-11e3-8475-00259028b818",
"2d432900-e267-11e3-894b-00259028b818",
"68393342-1bf1-11e4-ac0f-00259028b818",
"e4856c1a-63c0-11e4-a783-00259028b818",
"605fbf42-44af-11e4-b8fb-00259028b818",
"aeb63018-59ea-11e4-a01d-00259028b818",
"10302ed4-6585-11e4-9a42-00259028b818",
"b171b566-7191-11e4-a6ce-00259028b818",
"26487968-6f37-11e4-aecc-00259028b818",
"ab158970-e821-11e4-adfb-005056822e38",
"6d9b6e1a-f57e-11e4-9e4b-005056822e38",
"7a5caaca-02de-11e5-9040-005056822e38",
"cff297e8-047c-11e5-ba3f-005056822e38",
"5c79c2c2-037b-4a3e-aa13-84cc3310e76d",
"55382e9c-24c4-11e5-b56b-005056822e38",
"880a1cda-24c5-11e5-9901-005056822e38",
"a12dd33c-24c5-11e5-ac95-005056822e38",
"bb920c6a-24c6-11e5-a62b-005056822e38",
"89fae49c-3c4a-11e5-bafc-005056822e38",
"9a506ae6-4cc7-11e5-b643-005056822e38",
"ff162592-4d3f-11e5-983c-005056822e38",
"dabf9808-4d40-11e5-8c85-005056822e38",
"c748ccb6-4d42-11e5-bc84-005056822e38",
"3af5efbc-4d44-11e5-8540-005056822e38",
"3981f16a-4d46-11e5-af72-005056822e38",
"d2b8e228-47d6-11e5-8277-005056822e38",
"43bfb45a-1c04-11e5-a378-005056822e38",
"698e22e4-1c03-11e5-a0eb-005056822e38",
"4da30a92-ebb0-11e3-bb95-00259028b818",
)

wld = Region.objects.get(code='GLO')
for uuid in uuids:
    if ResourceBase.objects.filter(uuid=uuid).count() > 0:
        rb = ResourceBase.objects.get(uuid=uuid)
        print 'tagging %s' % rb.title
        rb.regions.add(wld)
    else:
        print '%s does not exist' % uuid
