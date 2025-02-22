from data import *
from datetime import datetime

def scan_purge_zones(purgelist):
    t = get_current_time()
    for uuid in zone_data:
        zone = zone_data[uuid]

        age = (t - zone["creation_date"]).days

        if zone["owner"] is None and zone["purgeable"] and not zone["private"] and (not zone["has_protected_block"] or (age >= 14 and zone["has_teleporters_only"])) and age >= 5:
            purgelist.append(uuid)

def scan_purge_zones_except_short_name_plain(purgelist):
    t = get_current_time()
    for uuid in zone_data:
        zone = zone_data[uuid]

        age = (t - zone["creation_date"]).days

        if zone["owner"] is None and zone["purgeable"] and not zone["private"] and (not zone["has_protected_block"] or (age >= 14 and zone["has_teleporters_only"])) and age >= 5 and (" " in zone["name"] or not zone["biome"] == "plain"):
            purgelist.append(uuid)