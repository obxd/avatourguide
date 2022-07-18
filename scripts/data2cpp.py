#/bin/env python

"""
git clone ao-bin-dumps to this dir to run the script
this script generate data.h and data.cpp
with maps name and description.
"""

import xml.etree.ElementTree as ET
import re
import sys

CACHE = dict()

ava_type_lexicon = {
 "TUNNEL_BLACK_LOW"    : "L1 Outer"
,"TUNNEL_LOW"          : "L2 Outer"
,"TUNNEL_BLACK_HIGH"   : "L1 Inner"
,"TUNNEL_HIGH"         : "L2 Inner"
,"TUNNEL_BLACK_MEDIUM" : "L1 Middle"
,"TUNNEL_MEDIUM"       : "L2 Middle"
,"TUNNEL_DEEP"         : "Deep"
,"TUNNEL_ROYAL"        : "Royal"
,"TUNNEL_HIDEOUT"      : "Rest"
,"TUNNEL_HIDEOUT_DEEP" : "Deep Rest"
}

def get_single_supported_layers(layers, supported_layers):
    match = ""
    c = 0
    for l in layers:
        for sl in supported_layers:
            if l == sl:
                c+=1
                match = l
    if c > 1:
        print(f"more than single layer match layers:{layers} supported layers:{supported_layers}", file=sys.stderr)
        exit(1)
    return match
        

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_big_blue_description(layers):
    layer = get_single_supported_layers(layers, ["Layer_01", "Layer_02", "Layer_03"])
    if   layer == "Layer_01": return "Big Blue T4"
    elif layer == "Layer_02": return "Big Blue T6"
    elif layer == "Layer_03": return "Big Blue T8"
    else:
        print(f"unsuported big blue layer {layer} ",file=sys.stderr)
        exit(1)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_big_gold_description(layers):
    layer = get_single_supported_layers(layers, ["Layer_01", "Layer_02"])
    if   layer == "Layer_01": return "Big Gold T8"
    elif layer == "Layer_02": return "Big Gold T6"
    else:
        print(f"unsuported big gold layer {layer} ",file=sys.stderr)
        exit(1)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_big_green_description(layers):
    layer = get_single_supported_layers(layers, ["Layer_01", "Layer_02", "Layer_03"])
    if   layer == "Layer_01": return "Big Green T8"
    elif layer == "Layer_02": return "Big Green T4"
    elif layer == "Layer_03": return "Big Green T6"
    else:
        print(f"unsuported big green layer {layer} ",file=sys.stderr)
        exit(1)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_group_dungeon_description(layers):
    layer = get_single_supported_layers(layers, ["Layer_01", "Layer_02", "Layer_03", "Layer_06", "Layer_07", "Layer_08", "Layer_09", "Layer_10", "Layer_11", "Layer_13", "Layer_14", "Layer_15"])
    if   layer == "Layer_01": return "Group Dungeon T8 Keeper"
    elif layer == "Layer_02": return "Group Dungeon T4 Keeper"
    elif layer == "Layer_03": return "Group Dungeon T6 Keeper"
    elif layer == "Layer_06": return "Group Dungeon T6 Heretic"
    elif layer == "Layer_07": return "Group Dungeon T4 Heretic"
    elif layer == "Layer_08": return "Group Dungeon T8 Heretic"
    elif layer == "Layer_09": return "Group Dungeon T6 Morgana"
    elif layer == "Layer_10": return "Group Dungeon T4 Morgana"
    elif layer == "Layer_11": return "Group Dungeon T8 Morgana"
    elif layer == "Layer_13": return "Group Dungeon T6 Undead"
    elif layer == "Layer_14": return "Group Dungeon T4 Undead"
    elif layer == "Layer_15": return "Group Dungeon T8 Undead"
    else:
        print(f"unsuported group dungeon layer {layer} ",file=sys.stderr)
        exit(1)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_ava_description(layers):
    layer = get_single_supported_layers(layers, ["Layer_01", "Layer_02"])
    if   layer == "Layer_01": return "AVA T6"
    elif layer == "Layer_02": return "AVA T8"
    else:
        print(f"unsuported ava layer {layer} ",file=sys.stderr)
        exit(1)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_solo_dungeon_description(layers):
    layer = get_single_supported_layers(layers, ["Layer_01", "Layer_02", "Layer_03", "Layer_06", "Layer_07", "Layer_08", "Layer_09", "Layer_10", "Layer_11", "Layer_12", "Layer_13", "Layer_14"])
    if   layer == "Layer_01": return "Solo Dungeon T8 Keeper"
    elif layer == "Layer_02": return "Solo Dungeon T4 Keeper"
    elif layer == "Layer_03": return "Solo Dungeon T6 Keeper"
    elif layer == "Layer_06": return "Solo Dungeon T6 Heretic"
    elif layer == "Layer_07": return "Solo Dungeon T4 Heretic"
    elif layer == "Layer_08": return "Solo Dungeon T8 Heretic"
    elif layer == "Layer_09": return "Solo Dungeon T6 Morgana"
    elif layer == "Layer_10": return "Solo Dungeon T4 Morgana"
    elif layer == "Layer_11": return "Solo Dungeon T8 Morgana"
    elif layer == "Layer_12": return "Solo Dungeon T6 Undead"
    elif layer == "Layer_13": return "Solo Dungeon T4 Undead"
    elif layer == "Layer_14": return "Solo Dungeon T8 Undead"
    else:
        print(f"unsuported solo dungeon layer {layer} ",file=sys.stderr)
        exit(1)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_small_chest_description(layers):
    layer = get_single_supported_layers(layers, ["Layer_01", "Layer_02", "Layer_03", "Layer_04", "Layer_05", "Layer_06"])
    if   layer == "Layer_01": return "Small Blue T8"
    elif layer == "Layer_02": return "Small Blue T6"
    elif layer == "Layer_03": return "Small Blue T4"
    elif layer == "Layer_04": return "Small Green T6"
    elif layer == "Layer_05": return "Small Green T8"
    elif layer == "Layer_06": return "Small Green T4"
    else:
        print(f"unsuported small chest layer {layer} ",file=sys.stderr)
        exit(1)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_small_gold_description(layers):
    layer = get_single_supported_layers(layers, ["Layer_01", "Layer_02"])
    if   layer == "Layer_01": return "Small Gold T6"
    elif layer == "Layer_02": return "Small Gold T8"
    else:
        print(f"unsuported small gold layer {layer} ",file=sys.stderr)
        exit(1)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_small_cave_description(layers):
    layer = get_single_supported_layers(layers, ["Layer_05", "Layer_07", "Layer_08", "Layer_15", "Layer_16", "Layer_17", "Layer_09", "Layer_10", "Layer_11", "Layer_18", "Layer_19", "Layer_20", "Layer_01", "Layer_02", "Layer_03", "Layer_04", "Layer_06", "Layer_12", "Layer_13", "Layer_14"])
    if   layer == "Layer_05": return "Big Group Hide/Ore T8 Node"
    elif layer == "Layer_07": return "Big Group Hide/Ore T7 Node"
    elif layer == "Layer_08": return "Big Group Hide/Ore T6 Node"
    elif layer == "Layer_15": return "Big Group Ore/Stone T8 Node"
    elif layer == "Layer_16": return "Big Group Ore/Stone T7 Node"
    elif layer == "Layer_17": return "Big Group Ore/Stone T6 Node"
    elif layer == "Layer_09": return "Big Raid Hide/Ore T7 Node"
    elif layer == "Layer_10": return "Big Raid Hide/Ore T8 Node"
    elif layer == "Layer_11": return "Big Raid Hide/Ore T6 Node"
    elif layer == "Layer_18": return "Big Raid Ore/Stone T7 Node"
    elif layer == "Layer_19": return "Big Raid Ore/Stone T8 Node"
    elif layer == "Layer_20": return "Big Raid Ore/Stone T6 Node"
    elif layer == "Layer_01": return "Solo Hide/Ore T8 Node"
    elif layer == "Layer_02": return "Solo Hide/Ore T6 Node"
    elif layer == "Layer_03": return "Solo Hide/Ore T7 Node"
    elif layer == "Layer_04": return "Solo Hide/Ore T5 Node"
    elif layer == "Layer_06": return "Solo Ore/Stone T6 Node"
    elif layer == "Layer_12": return "Solo Ore/Stone T8 Node"
    elif layer == "Layer_13": return "Solo Ore/Stone T7 Node"
    elif layer == "Layer_14": return "Solo Ore/Stone T5 Node"
    else:
        print(f"unsuported small cave layer {layer} ",file=sys.stderr)
        exit(1)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_small_clearing_description(layers):
    layer = get_single_supported_layers(layers, ["Layer_05", "Layer_07", "Layer_08", "Layer_15", "Layer_16", "Layer_17", "Layer_09", "Layer_10", "Layer_11", "Layer_18", "Layer_19", "Layer_20", "Layer_01", "Layer_02", "Layer_03", "Layer_04", "Layer_06", "Layer_12", "Layer_13", "Layer_14"])
    if   layer == "Layer_05": return "Big Group Fiber/Hide T8 Node"
    elif layer == "Layer_07": return "Big Group Fiber/Hide T7 Node"
    elif layer == "Layer_08": return "Big Group Fiber/Hide T6 Node"
    elif layer == "Layer_15": return "Big Group Wood/Fiber T8 Node"
    elif layer == "Layer_16": return "Big Group Wood/Fiber T7 Node"
    elif layer == "Layer_17": return "Big Group Wood/Fiber T6 Node"
    elif layer == "Layer_09": return "Big Raid Fiber/Hide T7 Node"
    elif layer == "Layer_10": return "Big Raid Fiber/Hide T8 Node"
    elif layer == "Layer_11": return "Big Raid Fiber/Hide T6 Node"
    elif layer == "Layer_18": return "Big Raid Wood/Fiber T7 Node"
    elif layer == "Layer_19": return "Big Raid Wood/Fiber T8 Node"
    elif layer == "Layer_20": return "Big Raid Wood/Fiber T6 Node"
    elif layer == "Layer_01": return "Solo Fiber/Hide T8 Node"
    elif layer == "Layer_02": return "Solo Fiber/Hide T6 Node"
    elif layer == "Layer_03": return "Solo Fiber/Hide T7 Node"
    elif layer == "Layer_04": return "Solo Fiber/Hide T5 Node"
    elif layer == "Layer_06": return "Solo Wood/Fiber T6 Node"
    elif layer == "Layer_12": return "Solo Wood/Fiber T7 Node"
    elif layer == "Layer_13": return "Solo Wood/Fiber T8 Node"
    elif layer == "Layer_14": return "Solo Wood/Fiber T5 Node"
    else:
        print(f"unsuported small clearing layer {layer} ",file=sys.stderr)
        exit(1)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_small_mountain_description(layers):
    layer = get_single_supported_layers(layers, ["Layer_05", "Layer_08", "Layer_07", "Layer_09", "Layer_10", "Layer_11", "Layer_01", "Layer_03", "Layer_04", "Layer_06"])
    if   layer == "Layer_05": return "Big Group Stone/Wood T6 Node"
    elif layer == "Layer_08": return "Big Group Stone/Wood T8 Node"
    elif layer == "Layer_07": return "Big Group Stone/Wood T7 Node"
    elif layer == "Layer_09": return "Big Group Stone/Wood T6 Node"
    elif layer == "Layer_10": return "Big Group Stone/Wood T7 Node"
    elif layer == "Layer_11": return "Big Group Stone/Wood T8 Node"
    elif layer == "Layer_01": return "Solo Stone/Wood T5 Node"
    elif layer == "Layer_03": return "Solo Stone/Wood T6 Node"
    elif layer == "Layer_04": return "Solo Stone/Wood T7 Node"
    elif layer == "Layer_06": return "Solo Stone/Wood T8 Node"
    else:
        print(f"unsuported small mountain layer {layer} ",file=sys.stderr)
        exit(1)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_medium_cave_description(layers):
    layer = get_single_supported_layers(layers, ["Layer_15", "Layer_16", "Layer_17", "Layer_25", "Layer_26", "Layer_27", "Layer_18", "Layer_19", "Layer_20", "Layer_28", "Layer_29", "Layer_30", "Layer_11", "Layer_12", "Layer_13", "Layer_14", "Layer_21", "Layer_22", "Layer_23", "Layer_24"])
    if   layer == "Layer_15": return "Big Group Hide/Ore T7 Node"
    elif layer == "Layer_16": return "Big Group Hide/Ore T8 Node"
    elif layer == "Layer_17": return "Big Group Hide/Ore T6 Node"
    elif layer == "Layer_25": return "Big Group Ore/Stone T7 Node"
    elif layer == "Layer_26": return "Big Group Ore/Stone T8 Node"
    elif layer == "Layer_27": return "Big Group Ore/Stone T6 Node"
    elif layer == "Layer_18": return "Big Raid Hide/Ore  T6 Node"
    elif layer == "Layer_19": return "Big Raid Hide/Ore T7 Node"
    elif layer == "Layer_20": return "Big Raid Hide/Ore T8 Node"
    elif layer == "Layer_28": return "Big Raid Ore/Stone T6 Node"
    elif layer == "Layer_29": return "Big Raid Ore/Stone T7 Node"
    elif layer == "Layer_30": return "Big Raid Ore/Stone T8 Node"
    elif layer == "Layer_11": return "Solo Hide/Ore T5 Node"
    elif layer == "Layer_12": return "Solo Hide/Ore T8 Node"
    elif layer == "Layer_13": return "Solo Hide/Ore T7 Node"
    elif layer == "Layer_14": return "Solo Hide/Ore U6 Node"
    elif layer == "Layer_21": return "Solo Ore/Stone T5 Node"
    elif layer == "Layer_22": return "Solo Ore/Stone T8 Node"
    elif layer == "Layer_23": return "Solo Ore/Stone T7 Node"
    elif layer == "Layer_24": return "Solo Ore/Stone T6 Node"
    else:
        print(f"unsuported medium cave layer {layer} ",file=sys.stderr)
        exit(1)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_medium_clearing_description(layers):
    layer = get_single_supported_layers(layers, ["Layer_03", "Layer_09", "Layer_10", "Layer_15", "Layer_16", "Layer_17", "Layer_25", "Layer_26", "Layer_27", "Layer_01", "Layer_02", "Layer_08", "Layer_18", "Layer_19", "Layer_20", "Layer_28", "Layer_29", "Layer_30", "Layer_04", "Layer_05", "Layer_06", "Layer_07", "Layer_11", "Layer_12", "Layer_13", "Layer_14", "Layer_21", "Layer_22", "Layer_23", "Layer_24"])
    if   layer == "Layer_03": return "Big Group Fiber/Hide T7 Node"
    elif layer == "Layer_09": return "Big Group Fiber/Hide T8 Node"
    elif layer == "Layer_10": return "Big Group Fiber/Hide T6 Node"
    elif layer == "Layer_15": return "Big Group Stone/Wood T7 Node"
    elif layer == "Layer_16": return "Big Group Stone/Wood T8 Node"
    elif layer == "Layer_17": return "Big Group Stone/Wood T6 Node"
    elif layer == "Layer_25": return "Big Group Wood/Fiber T7 Node"
    elif layer == "Layer_26": return "Big Group Wood/Fiber T8 Node"
    elif layer == "Layer_27": return "Big Group Wood/Fiber T6 Node"
    elif layer == "Layer_01": return "Big Raid Fiber/Hide T7 Node"
    elif layer == "Layer_02": return "Big Raid Fiber/Hide T6 Node"
    elif layer == "Layer_08": return "Big Raid Fiber/Hide T8 Node"
    elif layer == "Layer_18": return "Big Raid Stone/Wood T6 Node"
    elif layer == "Layer_19": return "Big Raid Stone/Wood T7 Node"
    elif layer == "Layer_20": return "Big Raid Stone/Wood T8 Node"
    elif layer == "Layer_28": return "Big Raid Wood/Fiber T6 Node"
    elif layer == "Layer_29": return "Big Raid Wood/Fiber T7 Node"
    elif layer == "Layer_30": return "Big Raid Wood/Fiber T8 Node"
    elif layer == "Layer_04": return "Solo Fiber/Hide T5 Node"
    elif layer == "Layer_05": return "Solo Fiber/Hide T8 Node"
    elif layer == "Layer_06": return "Solo Fiber/Hide T7 Node"
    elif layer == "Layer_07": return "Solo Fiber/Hide T6 Node"
    elif layer == "Layer_11": return "Solo Stone/Wood T7 Node"
    elif layer == "Layer_12": return "Solo Stone/Wood T5 Node"
    elif layer == "Layer_13": return "Solo Stone/Wood T8 Node"
    elif layer == "Layer_14": return "Solo Stone/Wood T6 Node"
    elif layer == "Layer_21": return "Solo Wood/Fiber T5 Node"
    elif layer == "Layer_22": return "Solo Wood/Fiber T8 Node"
    elif layer == "Layer_23": return "Solo Wood/Fiber T7 Node"
    elif layer == "Layer_24": return "Solo Wood/Fiber T6 Node"
    else:
        print(f"unsuported medium clearing layer {layer} ",file=sys.stderr)
        exit(1)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

templates_description_map= {
    # PVE
     "M_FR_ROAD_PVE_GROUP_01"         :get_big_blue_description
    ,"M_FR_ROAD_PVE_RAID_01"          :get_big_gold_description
    ,"M_FR_ROAD_PVE_SOLO_01"          :get_big_green_description
    ,"S_FR_ROAD_DNG_GROUP_Entrance_01":get_group_dungeon_description
    ,"S_FR_ROAD_DNG_RAID_Entrance_01" :get_ava_description
    ,"S_FR_ROAD_DNG_SOLO_Entrance_01" :get_solo_dungeon_description
    ,"S_FR_ROAD_PVE_Encounter_01"     :get_small_chest_description
    ,"S_FR_ROAD_PVE_Encounter_02"     :get_small_gold_description
    # Guthering stuff
    ,"S_FR_ROAD_RES_Cave_01"          :get_small_cave_description
    ,"S_FR_ROAD_RES_Clearing_01"      :get_small_clearing_description
    ,"S_FR_ROAD_RES_MountainSide_01"  :get_small_mountain_description
    ,"M_FR_ROAD_RES_Cave_01"          :get_medium_cave_description
    ,"M_FR_ROAD_RES_Clearing_01"      :get_medium_clearing_description
}

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_ava_clusters_elements():
    worldTree = ET.parse("./ao-bin-dumps/cluster/world.xml")
    worldRoot = worldTree.getroot()

    ava_clusters = list()
    for cluster in worldRoot.findall('.//clusters/cluster'):
        clusterType = cluster.attrib.get('type')
        if clusterType in ava_type_lexicon.keys():
            ava_clusters.append(cluster)

    # make sure we get all 400 maps
    assert len(set([x.attrib.get('displayname') for x in ava_clusters])) == 400
    return ava_clusters


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_claster_data(cluster :ET.Element):
    name = cluster.attrib.get('displayname')
    filename = cluster.attrib.get('file')
    tier = re.search(r"_T[4-8]_", filename).group(0).replace("_","")
    type = ava_type_lexicon[cluster.attrib.get("type")]

    if filename not in CACHE.keys():
        CACHE[filename] = ET.parse("./ao-bin-dumps/cluster/" + filename).getroot()

    cluster_root = CACHE[filename]

    items = list()
    for template in cluster_root.findall('.//templateinstance'):
        if template.attrib.get("ref") in templates_description_map.keys():
            active_layers = [ x.attrib.get("id") for x in template.findall("activelayer") ]
            filename = template.attrib.get("ref")
            items.append(templates_description_map[filename](active_layers)) 


    return {
        "name"   :name
        ,"tier"  :tier
        ,"type"  :type
        ,"items" :items
    }
        

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def write_data_h():
    with open("data.h",'w') as file:
        file.write("""
#ifndef DATA_H
#define DATA_H

#include <QString>
#include <iostream>
#include <vector>
using std::vector;
using std::string;

extern vector<QString> desc ;
extern vector<string> maps ;

#endif // DATA_H
""")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def write_data_cpp(maps):
    desc = "vector<QString> desc {"
    map_names = "vector<string> maps {"
    for i,map in enumerate(maps):
        map_names += '\n'
        desc += '\n'
        if i>0: 
            map_names += ','
            desc += ','
        map_names += '"' +  map["name"].lower().replace("-"," ") + '"'
        desc += '"'
        desc += f"<u>{map['name']} <b>{map['tier']}</b> {map['type']}</u><br>"
        desc += "<ul>"
        for item in map['items']:
            desc +="<li>" + item + "</li>" 
        desc += "</ul>"
        desc += '"'
            
    desc += '\n};'
    map_names += '\n};'

    with open("data.cpp",'w') as file:
        file.write('#include "data.h"' + '\n' +map_names + '\n' + desc + '\n')

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

if __name__ == "__main__":
    clusters = get_ava_clusters_elements()
    maps = list(map(get_claster_data, clusters))

    write_data_h()
    write_data_cpp(maps)
