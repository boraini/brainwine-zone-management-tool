import os
import json
import shutil

zone_data = {}
player_data = {}
players_by_block_hash = {}

config = None
with open("data.json") as c:
    config = json.load(c)

def java_hash(s):
    current = 0
    mult = 1
    for i in range(len(s) - 1, -1, -1):
        current += mult * ord(s[i])
        mult *= 31
    return current

def resolve(p):
    return config["run_directory"] + p

# load players into the zone_data object
for uuidjson in os.listdir(resolve("players/")):
    if not os.path.isfile(resolve("players/" + uuidjson)):
        continue

    uuid = uuidjson.split(".")[0]

    with open(resolve("players/" + uuidjson)) as p:
        dat = json.load(p)
        player_data[uuid] = dat
        players_by_block_hash[java_hash(uuid)] = dat

for d in os.listdir(resolve("zones/")):
    if not os.path.isdir(resolve("zones/" + d)):
        continue

    res = {}
    with open(resolve("zones/" + d + "/metablocks.json")) as f:
        obj = json.load(f)
        res["has_protected_block"] = any(["owner" in o and o["owner"] is not None for o in obj])
    with open(resolve("zones/" + d + "/config.json")) as f:
        obj = json.load(f)
        res["uuid"] = d
        res["name"] = obj["name"]
        res["private"] = obj["private"]
        res["owner"] = None if obj["owner"] is None else player_data[obj["owner"]]["name"]

    zone_data[d] = res

def find_uuid(zone_name):
    for uuid in zone_data:
        if zone_data[uuid]["name"] == zone_name:
            return uuid
        
    return None
def exclude_zone(zone_list, zone_name):
    result = find_uuid(zone_name)
    if result == None:
        print("Zone not found.")
        return
    
    while result in zone_list:
        zone_list.remove(result)

def include_zone(zone_list, zone_name):
    exclude_zone(zone_list, zone_name)
    
    result = find_uuid(zone_name)
    if result is not None:
        zone_list.append(result)

def scan_all_zones(zone_list = []):
    zone_list.clear()
    zone_list.extend(zone_data.keys())

def add_tabs(s, n):
    if s is None:
        return "\t" * n
    s = str(s)
    width = len(s) // 8
    return s + ("\t" * (n - width))

def print_zones(zone_list):
    keys = [("name", 3), ("uuid", 5), ("owner", 2), ("private", 1), ("has_protected_block", 3)]

    print("These zones will be deleted on the execution of the commit command: ")
    for my_key in keys:
        print(add_tabs(*my_key), end="")
    print()

    for uuid in zone_list:
        zone = zone_data[uuid]
        for my_key in keys:
            print(add_tabs(zone[my_key[0]], my_key[1]), end="")

        # line break
        print()

def delete_zones(zone_list):
    for uuid in zone_list:
        shutil.rmtree(resolve("zones/" + uuid))

def print_player(player_name):
    for uuid in player_data:
        if player_data[uuid]["name"] == player_name:
            print(f"UUID of player {player_name} is {uuid}")
            return

    print("Player not found!")
