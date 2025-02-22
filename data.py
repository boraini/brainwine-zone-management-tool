import os
import json
import shutil
from dateutil.parser import isoparse
from datetime import datetime, timezone

zone_data = {}
player_data = {}
players_by_block_hash = {}

config = None
with open("data.json") as c:
    config = json.load(c)

def get_current_time():
    return datetime.now(timezone.utc)

def java_hash(s):
    current = 0
    for chr in s:
        current = (31 * current + ord(chr)) & (2**32 - 1)
        if current & 2**31:
            current -= 2**32
    return current

def java_mod(n, m):
    if n < 0:
        return (m % m) - m
    else:
        return n % m

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
        res["has_teleporters_only"] = not any(["owner" in o and o["owner"] is not None and o["item"] != "mechanical/teleporter" for o in obj])
        res["has_protected_block"] = any(["owner" in o and o["owner"] is not None and (o["item"].startswith("mechanical/dish") or o["item"] == "mechanical/teleporter") for o in obj])
        
    with open(resolve("zones/" + d + "/config.json")) as f:
        obj = json.load(f)
        res["uuid"] = d
        res["name"] = obj["name"]
        res["biome"] = obj["biome"]
        res["private"] = obj["private"]
        res["owner"] = None if obj["owner"] is None else player_data[obj["owner"]]["name"]
        res["purgeable"] = not ("rules" in obj and "purgeable" in obj["rules"] and not obj["rules"]["purgeable"])
        
        try:
            res["creation_date"] = isoparse(obj["creation_date"])
        except:
            res["creation_date"] = get_current_time()
        try:
            res["last_active_date"] = isoparse(obj["last_active_date"])
        except:
            res["last_active_date"] = get_current_time()

    zone_data[d] = res

def find_uuid(zone_name):
    for uuid in zone_data:
        if zone_data[uuid]["name"] == zone_name:
            return uuid
        
def find_uuid_by_player(player_name, zone_name):
    for uuid in zone_data:
        if zone_data[uuid]["owner"] == player_name and zone_data[uuid]["name"] == zone_name:
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

def include_zone_by_player(zone_list, player_name, zone_name):
    result = find_uuid_by_player(player_name, zone_name)
    if result is not None:
        zone_list.append(result)

def scan_all_zones(zone_list = []):
    zone_list.clear()
    zone_list.extend(zone_data.keys())

def scan_owned_by(zone_list, player_name):
    zone_list.extend([uuid for uuid in zone_data.keys() if zone_data[uuid]["owner"] == player_name])

def add_tabs(s, n):
    if s is None:
        return "None" + ("\t" * (n - 1))
    s = str(s)
    width = len(s) // 8
    return s + ("\t" * (n - width))

def print_zones(zone_list):
    keys = [("name", 3), ("uuid", 5), ("owner", 3), ("private", 1), ("has_protected_block", 3), ("has_teleporters_only", 3), ("creation_date", 5), ("biome", 1)]

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

    print(f"There are {len(zone_list)} zones in the list.")

def delete_zones(zone_list):
    for uuid in zone_list:
        shutil.rmtree(resolve("zones/" + uuid))

def find_player_by_owner_hash(owner_hash):
    for uuid in player_data:
        print(java_mod((java_hash(uuid) & 2047), 2047))
        if owner_hash == 1 + java_mod((java_hash(uuid) & 2047), 2047):
            player_name = player_data[uuid]["name"]
            print(f"Player {player_name} with uuid {uuid} has owner hash {owner_hash}.")
            return
        
    print("No such owner hash found")

def print_player(player_name):
    for uuid in player_data:
        if player_data[uuid]["name"] == player_name:
            print(f"UUID of player {player_name} is {uuid}")
            return

    print("Player not found!")
