#!/usr/bin/env python3
import sys, os, io
import xml.etree.ElementTree as ET
import argparse
from configparser import ConfigParser
from os import walk
from datetime import datetime
from gamelist.gamelist import RPGameList, GLBrowser
from shutil import copyfile
###############################################################################
LOG_FILE = "gltool.log"
DEFAULT_GAMELIST_FILE_NAME = 'new_gamelist.xml'
UseConsoleOut=False
###############################################################################
def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(msg + "\n")
    if not UseConsoleOut: print(msg)


def out_gl_file_name(name=None):
    if name: 
        return name + '.new'
    else:
        return DEFAULT_GAMELIST_FILE_NAME


def create_file_bak(fpath):
    fnewpathExt = datetime.now().strftime('.%d-%m-%y_%H-%M-%S')
    fnewpath = fpath + fnewpathExt
    #copyfile(fpath, fnewpath)
    os.rename(fpath, fnewpath)
    log("+ Saved original file {} to {}".format(fpath, fnewpath))


def print_file(gamelist):
    print(gamelist.to_xml())


def create_file(gamelist, fpath, backup=True):
    if backup: create_file_bak(fpath)
    gamelist.write(fpath)
    log("+ Wrote gamelist in {}".format(fpath))

def get_image_files_in_tree(dpath):
    flist = []
    for (rep, subreps, files) in walk(dpath):
        flist.extend([os.path.join(rep, f).replace('\\','/') for f in files if f.endswith('.png')])
    return flist


def get_image_files_in_tree_as_map(dpath):
    flist = {}
    for (rep, subreps, files) in walk(dpath):
        flist.update({f[:-4]:os.path.join(rep, f).replace('\\','/') for f in files if f.endswith('.png')})
    return flist


def complete_empty_image_path(fpath, gamelist=None):
    log("+ Complete missing game images on {}".format(fpath))
    #get image paths from disk
    #FIXME: image path should be relative to game path: not the case here,
    # we get a full path from search dir
    dpath = os.path.dirname(fpath) or '.'
    prefixLen = 0 if dpath == '.' or dpath == './' else len(dpath) + 1
    img_dic = get_image_files_in_tree_as_map(dpath)
    #get game list with empty images
    gl = gamelist or RPGameList.from_path(fpath)
    #complete game list with found images
    for g in GLBrowser(gl).get_empty_image_games():
        log('Missing image game: {}'.format(g.name()))
        if g.name() in img_dic:
            imagePath = img_dic[g.name()][prefixLen:]
            log('Found image game: {} -> {}'.format(g.name(), imagePath))
            g.image(imagePath)
    return gl


def list_target(fpath, target):
    gl = GLBrowser(RPGameList.from_path(fpath))
    if target == 'image':
        print("\n".join([i for i in gl.get_game_images()]))
    if target == 'game':
        print(''.join(["{}\n\t{}/{} '{}'\n".format(g.name(), g.region(), g.genre(), g.path()) for g in gl.get_games()]))
    if target == 'folder':
        print(''.join(["{}\n\t'{}' '{}'\n".format(g.name(), g.thumbnail(), g.path()) for g in gl.get_folders()]))
    if target == 'empty_image':
        print("\n".join(["{}: {}".format(g.name(), g.path()) for g in gl.get_empty_image_games()]))


def merge_gamelist(gamelist, keep_doublons=False):
    log("+ Merging gamelist(s) {}".format(gamelist[:0]))
    root = ET.Element('gamelist')
    g_dic= {}
    #g_dic.append({k,v for })#TODO
    for glpath in gamelist:
        for f in RPGameList.from_path(glpath).get_folders():
            g_dic[f.path()] = f
        for g in RPGameList.from_path(glpath).get_games():
            g_dic[g.path()] = g

    for (k,v) in g_dic:
        ET.SubElement(root, v)
        
    return RPGameList(root)


def check_missing_games(glpath, gamelist=None):
    log("+ Check missing game paths on {}".format(glpath))
    pathdir = os.path.dirname(glpath)
    root = ET.Element('gamelist')
    g_dic= {}
    gl = gamelist or RPGameList.from_path(glpath)
    glg = gl.get_games()
    #
    for g in glg:
        gpath = os.path.join(pathdir, g.path())
        if not os.path.exists(gpath):
            log("Missing ROM file for game {}. Declared path: {}".format(g.name(), g.path()))
            g.delete()
    #
    return gl

###############################################################################
def main ():
    global UseConsoleOut
    parser = argparse.ArgumentParser(description='Helpful tool for managing and cleaning gamelist.xml file(s)')
    parser.add_argument('--clear', help='clear specified element', type=str, choices=['game', 'title', 'image'], default='')
    parser.add_argument('--delete', help='delete game(s) that match selector', type=str)
    parser.add_argument('-l', '--list', help='list the game(s) matching selector', type=str, default='', nargs='?')
    parser.add_argument('--count', help='execute the specified command', type=str, default='', nargs='?')
    parser.add_argument('--repair', help='fix paths issue for games', type=str, choices=['game', 'image', 'all'], nargs='+', default='')
    parser.add_argument('--merge', help='execute the specified command', action='store_true', default=False)
    parser.add_argument('-o', '--console', help='Output result on console (no disk write)', action='store_true', default=False)
    #parser.add_argument('target', help='affect the specified element', choices=['game', 'description', 'title', 'image', 'empty_image', 'folder'])
    parser.add_argument('-f', '--files', dest='gamelist', help='the gamelist.xml(s) path(s)', default='gamelist.xml', nargs='*')
    args = parser.parse_args()
    #
    glpath = args.gamelist[0]
    UseConsoleOut = args.console or False
    if args.list:
        list_target(glpath, args.list)
    if args.repair:
        gl = None
        if any(item in args.repair for item in ['game', 'all']):
            gl = check_missing_games(glpath, gamelist=gl)
        if any(item in args.repair for item in ['image', 'all']):
            gl = complete_empty_image_path(glpath, gamelist=gl)
        #write output new file
        if UseConsoleOut:
            print_file(gl)
        else:
            create_file(gl, glpath)
    if args.merge:
        gl = merge_gamelist(args.gamelist)
        gl.write(out_gl_file_name())

###
if __name__ == "__main__":
    main()
