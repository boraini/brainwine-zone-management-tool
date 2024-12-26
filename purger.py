from data import *

def scan_purge_zones(purgelist):
    for uuid in zone_data:
        zone = zone_data[uuid]

        if zone["owner"] is None and not zone["private"] and not zone["has_protected_block"]:
            purgelist.append(uuid)