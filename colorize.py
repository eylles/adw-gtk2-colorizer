#!/usr/bin/env python3

import json
import argparse
import sys
import os


#############
# functions #
#############

def data_sub_link(dictio, key, value):
    """
    return type: void
    description:
      replace the "@key_name" links
      with the color string value of
      the refferenced key
    """
    if value.find("@") > -1:
        index_str = value[1:]
        dictio[key] = dictio[index_str]
        if args.debug:
            print("{k}: {v}".format(k=key, v=dictio[key]))


def data_rgb_to_hex(dictio, key, value):
    """
    return type: void
    description:
      replace the "rgba()" values
      with the correspinding rgb hex string
    """
    if value.find("rgb") > -1:
        oparen = value.find("(")
        cparen = value.find(")")
        # index_str = value[1:]
        vallist = value[oparen+1:cparen].split(",")
        r = int(vallist[0])
        g = int(vallist[1])
        b = int(vallist[2])
        res = "#{0:02x}{1:02x}{2:02x}".format(r, g, b)
        dictio[key] = res
        if args.debug:
            print("{k}: {v}".format(
                k=key, v=dictio[key]))


########
# Main #
########

# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument("-f", "--file", required="true", help="JSON file to use")
parser.add_argument("-r", "--resources", dest="res", required="true",
                    help="adw-gtk2 dir")
parser.add_argument("-d", "--debug", action='store_true',
                    help="Show Debug Output")

# Read arguments from command line
args = parser.parse_args()

if args.debug:
    print("Displaying Debug Output of % s" % parser.prog)
    print("File '{}' selected".format(args.file))

with open(args.file) as json_file:
    data = json.load(json_file)
    if args.debug:
        print("Data read from file:", args.file)
        print("Name:", data["name"])
        # print("Vars:", data["variables"])
        for keys, values in data["variables"].items():
            print("{key: >24}: {value}".format(key=keys, value=values))

# correct data
for keys, values in data["variables"].items():
    data_sub_link(data["variables"], keys, values)
for keys, values in data["variables"].items():
    data_rgb_to_hex(data["variables"], keys, values)


if args.debug:
    print("Corrected Data:")
    print("Name:", data["name"])
    # print("Vars:", data["variables"])
    for keys, values in data["variables"].items():
        print("{key: >24}: {value}".format(key=keys, value=values))

search_dark = {
    "text": "white",
    "base": "#232729",
    "fg": "#eeeeec",
    "bg": "#33393b",
    "selection_fg": "#ffffff",
    "selection_bg": "#215d9c",
    "insensitive_fg": "#919494",
    "insensitive_bg": "#2d3234",
    "menu": "#262b2d",
    "link": "#4a90d9",
    "link_visited": "#2a76c6",
    "column_header": "#898b8b",
    "column_header_hover": "#bcbdbc",
    "window_color": "#2c3133",
    "tooltip_fg": "#ffffff",
    "tooltip_bg": "#343434",
}

replace_dark = {
    "text": data["variables"]["window_fg_color"],
    "base": data["variables"]["window_bg_color"],
    "fg": data["variables"]["view_fg_color"],
    "bg": data["variables"]["view_bg_color"],
    "selection_fg": data["variables"]["card_bg_color"],
    "selection_bg": data["variables"]["accent_color"],
    "insensitive_fg": data["variables"]["accent_fg_color"],
    "insensitive_bg": data["variables"]["shade_color"],
    "menu": data["variables"]["view_bg_color"],
    "link": data["variables"]["accent_color"],
    "link_visited": data["variables"]["accent_fg_color"],
    "column_header": data["variables"]["headerbar_shade_color"],
    "column_header_hover": data["variables"]["shade_color"],
    "window_color": data["variables"]["card_bg_color"],
    "tooltip_fg": data["variables"]["window_fg_color"],
    "tooltip_bg": data["variables"]["window_bg_color"],
}

gtk_rc = "{}/adw-gtk3/gtk-2.0/gtkrc".format(args.res)
gtk_dark_rc = "{}/adw-gtk3-dark/gtk-2.0/gtkrc".format(args.res)

username = os.environ['USER']
home_dir = os.environ.get('HOME', '/home/{}'.format(username))

"""
i will assume that the command to install adw-gtk2 was:
make install INSTALL_DIR=~/.local/share/themes
"""
target_dir = "{}/.local/share/themes".format(home_dir)
target = "{}/adw-gtk3/gtk-2.0/gtkrc".format(target_dir)
target_dark = "{}/adw-gtk3-dark/gtk-2.0/gtkrc".format(target_dir)

if os.path.exists(args.res):
    # print("dir exists")
    if os.path.isfile(gtk_rc) and os.path.isfile(gtk_dark_rc):
        if args.debug:
            print("rc files exist")
        with open(gtk_dark_rc, 'r') as file:
            data = file.read()
            for keys, values in search_dark.items():
                # print("{}: {}".format(keys, values))
                data = data.replace(search_dark[keys], replace_dark[keys])
            if args.debug:
                print(data)
        with open(target_dark, 'w') as file:
            file.write(data)
    else:
        print("rc files don't exist")
        sys.exit()
else:
    print("invalid dir: {}".format(args.res))
    sys.exit()
