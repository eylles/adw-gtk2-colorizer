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


def colorize_gtk2(gtkrc_file, target_rc, search_dict):
    """
    return type: void
    Description:
      replace the colors on the gtk rc file specified
      in "gtkrc_file" using the provided "search_dict"
      with the colors from the global "replace" dict,
      write the file to the "target_rc" gtkrc file
    """
    with open(gtkrc_file, 'r') as file:
        data = file.read()
        for keys, values in search_dict.items():
            # print("{}: {}".format(keys, values))
            data = data.replace(search_dict[keys], replace[keys])
        if args.debug:
            print(data)
    with open(target_rc, 'w') as file:
        file.write(data)


########
# Main #
########

# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument("-f", "--file", required="true", help="JSON file to use")
parser.add_argument("-r", "--resources", dest="res", required="true",
                    help="adw-gtk2 dir")
parser.add_argument("-t", "--target", dest="targ",
                    help="should be the PARENT dir "
                         "containing the 'adw-gtk3' and 'adw-gtk3-dark' dirs")
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
    # Text/base
    "text_color": "white",
    "base_color": "#232729",

    # Foreground/background
    "fg_color": "#eeeeec",
    "bg_color": "#33393b",

    # Tooltips
    "tooltip_fg_color": "#ffffff",
    "tooltip_bg_color": "#343434",

    # Selected foreground/background
    "selected_fg_color": "#ffffff",
    "selected_bg_color": "#215d9c",

    # Insensitive foreground/background
    "insensitive_fg_color": "#919494",
    "insensitive_bg_color": "#2d3234",

    # Menubar
    "menubar_bg_color": "#262b2d",
    "menubar_fg_color": "#ffffff",

    # Toolbar
    "toolbar_bg_color": "#262b2d",
    "toolbar_fg_color": "#ffffff",

    # Menus
    "menu_color": "#262b2d",
    "menu_bg_color": "#262b2d",
    "menu_fg_color": "#ffffff",

    # Panel
    "panel_bg_color": "#262b2d",
    "panel_fg_color": "#ffffff",

    # Links
    "link_color": "#4a90d9",
    "visited_link_color": "#2a76c6",

    # button
    "btn_bg_color": "#343434",
    "btn_fg_color": "#eeeeec",

    # titlebar
    "titlebar_bg_color": "#262b2d",
    "titlebar_fg_color": "#ffffff",

    # caret
    "primary_caret_color": "#eeeeec",
    "secondary_caret_color": "#ffffff",

    # accent
    "accent_bg_color": "#4a90d9",

    # Treeview headers
    "column_header_color": "#898b8b",
    "hover_column_header_color": "#bcbdbc",

    # Window decoration
    "window_color": "#2c3133",
}

search_light = {
    # Text/base
    "text_color": "black",
    "base_color": "white",

    # Foreground/background
    "fg_color": "#2e3436",
    "bg_color": "#fafafa",

    # Tooltips
    "tooltip_fg_color": "#ffffff",
    "tooltip_bg_color": "#343434",

    # Selected foreground/background
    "selected_fg_color": "#ffffff",
    "selected_bg_color": "#3584e4",

    # Insensitive foreground/background
    "insensitive_fg_color": "#8b8e8f",
    "insensitive_bg_color": "#f0f0f0",

    # Menubar
    "menubar_bg_color": "#eeeeee",
    "menubar_fg_color": "black",

    # Toolbar
    "toolbar_bg_color": "#eeeeee",
    "toolbar_fg_color": "black",

    # Menus
    "menu_color": "white",
    "menu_bg_color": "#eeeeee",
    "menu_fg_color": "black",

    # Panel
    "panel_bg_color": "#fafafa",
    "panel_fg_color": "black",

    # Links
    "link_color": "#2a76c6",
    "visited_link_color": "#215d9c",

    # button
    "btn_bg_color": "#eeeeee",
    "btn_fg_color": "black",

    # titlebar
    "titlebar_bg_color": "#fafafa",
    "titlebar_fg_color": "black",

    # caret
    "primary_caret_color": "#2e3436",
    "secondary_caret_color": "#000000",

    # accent
    "accent_bg_color": "#2a76c6",

    # Treeview headers
    "column_header_color": "#979a9b",
    "hover_column_header_color": "#636769",

    # Window decoration
    "window_color": "#f4f4f4",
}

replace = {
    # Text/base
    "text_color": data["variables"]["window_fg_color"],
    "base_color": data["variables"]["view_bg_color"],

    # Foreground/background
    "fg_color": data["variables"]["view_fg_color"],
    "bg_color": data["variables"]["window_bg_color"],

    # Selected foreground/background
    "selected_fg_color": data["variables"]["card_bg_color"],
    "selected_bg_color": data["variables"]["accent_color"],

    # Insensitive foreground/background
    "insensitive_fg_color": data["variables"]["accent_fg_color"],
    "insensitive_bg_color": data["variables"]["shade_color"],

    # Menus
    "menu_color": data["variables"]["window_bg_color"],
    "menu_bg_color": data["variables"]["window_bg_color"],
    "menu_fg_color": data["variables"]["view_fg_color"],

    # Menubar
    "menubar_bg_color": data["variables"]["view_bg_color"],
    "menubar_fg_color": data["variables"]["view_fg_color"],

    # Panel
    "panel_bg_color": data["variables"]["window_bg_color"],
    "panel_fg_color": data["variables"]["view_fg_color"],

    # Toolbar
    "toolbar_bg_color": data["variables"]["card_bg_color"],
    "toolbar_fg_color": data["variables"]["view_fg_color"],

    # Links
    "link_color": data["variables"]["accent_color"],
    "visited_link_color": data["variables"]["accent_fg_color"],

    # accent
    "accent_bg_color": data["variables"]["accent_color"],

    # Treeview headers
    "column_header_color": data["variables"]["headerbar_shade_color"],
    "hover_column_header_color": data["variables"]["shade_color"],

    # Window decoration
    "window_color": data["variables"]["card_bg_color"],

    # Tooltips
    "tooltip_bg_color": data["variables"]["window_bg_color"],
    "tooltip_fg_color": data["variables"]["window_fg_color"],

    # button
    "btn_bg_color": data["variables"]["shade_color"],
    "btn_fg_color": data["variables"]["view_fg_color"],

    # titlebar
    "titlebar_bg_color": data["variables"]["window_bg_color"],
    "titlebar_fg_color": data["variables"]["view_fg_color"],

    # caret
    "primary_caret_color": data["variables"]["view_fg_color"],
    "secondary_caret_color": data["variables"]["window_fg_color"],

}

gtk_rc = "{}/adw-gtk3/gtk-2.0/gtkrc".format(args.res)
gtk_dark_rc = "{}/adw-gtk3-dark/gtk-2.0/gtkrc".format(args.res)

if args.targ:
    target_dir = "{}".format(args.targ)
else:
    """
    i will assume that the command to install adw-gtk2 was:
    make install INSTALL_DIR=~/.local/share/themes
    """
    username = os.environ['USER']
    home_dir = os.environ.get('HOME', '/home/{}'.format(username))
    target_dir = "{}/.local/share/themes".format(home_dir)


target_light = "{}/adw-gtk3/gtk-2.0/gtkrc".format(target_dir)
target_dark = "{}/adw-gtk3-dark/gtk-2.0/gtkrc".format(target_dir)

if os.path.exists(args.res):
    if args.debug:
        print("dir exists")
    if os.path.isfile(gtk_rc) and os.path.isfile(gtk_dark_rc):
        if args.debug:
            print("rc files exist")
        # colorize light
        colorize_gtk2(gtk_rc, target_light, search_light)
        # colorize dark
        colorize_gtk2(gtk_dark_rc, target_dark, search_dark)
        if args.debug:
            print("rc files written")
    else:
        print("rc files don't exist")
        sys.exit()
else:
    print("invalid dir: {}".format(args.res))
    sys.exit()
