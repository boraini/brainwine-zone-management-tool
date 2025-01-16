from data import *


def scan_short_name_plain_zones(purgelist):
    for uuid in zone_data:
        zone = zone_data[uuid]

        if zone["biome"] == "plain" and " " not in zone["name"]:
            purgelist.append(uuid)