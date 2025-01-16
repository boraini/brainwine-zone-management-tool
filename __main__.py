from purger import *
from data import *
from short_name_plain import *

HELP = """Zone Management Tool
stop: stops the tool
show: shows the latest list of zones to be purged
player [player name]: shows the UUID of the given player
clear: clears the list of zones to be purged
scan purge: adds zones determined to be purged
scan all: adds ALL zones for purging
exclude [zone name]: excludes zone from purging
include [zone name]: includes zone for purging
commit: deletes the zones
"""

purgelist = []

print(HELP)

while True:
    cmd = input("")

    if cmd == "help":
        print(HELP)
        continue

    if cmd == "stop":
        break

    if cmd == "show":
        print_zones(purgelist)
        continue

    if cmd == "clear":
        purgelist = []
        continue
    
    if cmd == "scan purge":
        scan_purge_zones(purgelist)
        continue

    if cmd == "scan short name plain":
        scan_short_name_plain_zones(purgelist)
        continue

    if cmd == "scan purge except short name plain":
        scan_purge_zones_except_short_name_plain(purgelist)
        continue

    if cmd == "scan all":
        scan_all_zones(purgelist)
        continue

    if cmd.startswith("exclude"):
        zone_name = cmd[len("exclude "):].lstrip().rstrip()
        exclude_zone(purgelist, zone_name)
        continue
    
    if cmd.startswith("include"):
        zone_name = cmd[len("include "):].lstrip().rstrip()
        include_zone(purgelist, zone_name)
        continue

    if cmd.startswith("player"):
        player_name = cmd[len("player "):].lstrip().rstrip()
        print_player(player_name)
        continue

    if cmd == "commit":
        print("Are you sure? There is no way back! Input \"yes\" to continue.")
        if input() == "yes":
            delete_zones(purgelist)
            print("Zones have been deleted. Exiting...")
            break
        continue

    print("Invalid command: " + cmd)
