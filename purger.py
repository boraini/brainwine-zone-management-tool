from data import *
from datetime import datetime

def scan_purge_zones(purgelist):
    t = get_current_time()
    for uuid in zone_data:
        zone = zone_data[uuid]

        if zone["owner"] is None and not zone["private"] and not zone["has_protected_block"] and (t - zone["creation_date"]).days >= 5:
            purgelist.append(uuid)

def scan_purge_zones_except_short_name_plain(purgelist):
    t = get_current_time()
    for uuid in zone_data:
        zone = zone_data[uuid]

        if zone["owner"] is None and not zone["private"] and not zone["has_protected_block"] and (t - zone["creation_date"]).days >= 5 and (" " in zone["name"] or not zone["biome"] == "plain"):
            purgelist.append(uuid)