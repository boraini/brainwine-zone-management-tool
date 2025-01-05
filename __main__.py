from purger import *
from data import *

HELP = """Zone Management Tool
stop: stops the tool
show: shows the latest list of zones to be purged
clear: clears the list of zones to be purged
scan purge: adds zones determined to be purged
exclude [zone name]: excludes zone from purging
include [zone name]: includes zone from purging
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

    if cmd == "scan all":
        scan_all_zones(purgelist)
        continue

    if cmd.startswith("exclude"):
        zone_name = cmd[len("exclude "):].lstrip().rstrip()
        exclude_zone(purgelist, zone_name)
        continue
    
    if cmd.startswith("include"):
        zone_name = cmd[len("exclude "):].lstrip().rstrip()
        include_zone(purgelist, zone_name)
        continue

    if cmd == "commit":
        print("Are you sure? There is no way back! Input \"yes\" to continue.")
        if input() == "yes":
            delete_zones(purgelist)
            print("Zones have been deleted. Exiting...")
            break
        continue

    print("Invalid command: " + cmd)
