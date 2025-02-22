from data import *
from datetime import datetime

def should_purge(zone):
    t = get_current_time()
    age = (t - zone["creation_date"]).days
    return zone["owner"] is None and zone["purgeable"] and not zone["private"] and (not zone["has_protected_block"] or (age >= 14 and zone["has_teleporters_only"])) and age >= 5

def is_short_name_plain(zone):
    return (not " " in zone["name"]) and zone["biome"] == "plain"

def scan_purge_zones(purgelist):
    for uuid in zone_data:
        zone = zone_data[uuid]

        if should_purge(zone):
            purgelist.append(uuid)

def scan_purge_zones_except_short_name_plain(purgelist):
    for uuid in zone_data:
        zone = zone_data[uuid]

        if should_purge(zone) and not is_short_name_plain(zone):
            purgelist.append(uuid)
