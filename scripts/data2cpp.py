#/bin/env python

"""
git clone ao-bin-dumps to this dir to run the script
this script generate data.h and data.cpp
with maps name and description.
"""

import xml.etree.ElementTree as ET
import re
import sys

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

chest_color = {
     "Solo" :"Green"
    ,"Group":"Blue"
    ,"Raid" :"Gold"
}

dungeon_type = {
     "HER" : "Heretic"
    ,"KPR" : "Keeper"
    ,"MOR" : "Morgana"
    ,"UND" : "Undead"
}

resource_type = {
     "Solo"  : "Small"
    ,"Group" : "Big"
    ,"Raid"  : "Big Raid"
}


templates={
    # PVE
    # small chests
     "S_FR_ROAD_PVE_Encounter_01"     :"Small"
    ,"S_FR_ROAD_PVE_Encounter_02"     :"Small"
    # big chests
    ,"M_FR_ROAD_PVE_SOLO_01"          :"Big Green"
    ,"M_FR_ROAD_PVE_GROUP_01"         :"Big Blue"
    ,"M_FR_ROAD_PVE_RAID_01"          :"Big Gold"
    # dungeons 
    ,"S_FR_ROAD_DNG_SOLO_Entrance_01" :"Solo"
    ,"S_FR_ROAD_DNG_GROUP_Entrance_01":"Group"
    ,"S_FR_ROAD_DNG_RAID_Entrance_01" :"AVA"
    # Guthering stuff
    ,"S_FR_ROAD_RES_Cave_01"          :"Node"
    ,"S_FR_ROAD_RES_Clearing_01"      :"Node"
    ,"S_FR_ROAD_RES_MountainSide_01"  :"Node"
    ,"M_FR_ROAD_RES_Cave_01"          :"Node"
    ,"M_FR_ROAD_RES_Clearing_01"      :"Node"
}

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

CACHE = dict()
def cache_or_get_from_cache(path):
    if path not in CACHE.keys():
        CACHE[path] = ET.parse(path)
    return CACHE[path]


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_tier_from_string(string):
    matches = re.search(r"T[4-8]", string)
    if matches:
        return matches.group(0)
    else:
        print(f"Unable to get tier from str:'{string}'",file=sys.stderr)
        exit(1)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def ger_resource_tier_from_string(string):
    matches = re.search(r"T([4-8]|/)+", string)
    if matches:
        return "T" + matches.group(0)[-1]
    else:
        print(f"Unable to get tier from str:'{string}'",file=sys.stderr)
        exit(1)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def format_description(tag, parentname, childname):
    if "Big" in tag:
        return  tag + " " +  get_tier_from_string(childname)

    elif "Small" ==  tag:
        return tag + " " + chest_color[parentname.split(" ")[0]] + " " + get_tier_from_string(childname)

    elif tag in ("Solo","Group"):
        return tag + " Dungeon "+ get_tier_from_string(childname) + " " + dungeon_type[childname[-3:]]

    elif tag == 'AVA':
        return tag +" " + get_tier_from_string(childname)

    else:
        return tag + ": " + resource_type[parentname] +  " " + childname.split(" ")[0] + " " + ger_resource_tier_from_string(childname)


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

def find_non_layout_elem(elem:ET.ElementTree , layers):
    for layer in layers: 
        parentEl = elem.find(f"./tiles/*/layer[@id='{layer}']/..")
        if parentEl == None:
            print(f"unable to find layer in element",file=sys.stderr)
            exit(1)
        elif parentEl.attrib.get("name") != "Layout":
            return  parentEl,layer

    print(f"unable to find non layout layer",file=sys.stderr)
    exit(1)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_parent_child_names(elem, layer):
    parent = elem.attrib.get("name")
    el = elem.find(f"./layer[@id='{layer}']")
    if el == None:
        print(f"unable to find layer in element",file=sys.stderr)
        exit(1)
    child = el.attrib.get("name")
    return parent, child


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_templates_description_map(filename,layers):
    tag = templates[filename]
    path = "ao-bin-dumps/templates/NONE/" + filename + ".template.xml"
    elemTree = cache_or_get_from_cache(path)
    elm,layer = find_non_layout_elem(elemTree, layers)
    parent, child = get_parent_child_names(elm, layer)
    return format_description(tag, parent, child)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_claster_data(cluster :ET.Element):
    name = cluster.attrib.get('displayname')
    filename = cluster.attrib.get('file')
    tier = get_tier_from_string(filename)
    type = ava_type_lexicon[cluster.attrib.get("type")]
    cluster_et = cache_or_get_from_cache("./ao-bin-dumps/cluster/" + filename)
    cluster_root = cluster_et.getroot()

    items = list()
    for template in cluster_root.findall('.//templateinstance'):
        if template.attrib.get("ref") in templates.keys():
            active_layers = [ x.attrib.get("id") for x in template.findall("activelayer") ]
            filename = template.attrib.get("ref")
            items.append(get_templates_description_map(filename,active_layers)) 

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

def sort_key(string):
    tag  = string.split(" ")[0].replace(":","")
    tag_order ={
         "Small" : 1
        ,"Big"   : 2
        ,"Solo"  : 3
        ,"Group" : 4
        ,"AVA"   : 5
        ,"Node"  : 6 }
    return tag_order[tag]

        

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
        for item in sorted(map['items'], key=sort_key):
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
