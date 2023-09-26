#!/usr/bin/env python3
import sys
import os
import io
from typing import List, Mapping as Map
import xml.etree.ElementTree as ET
import argparse
from configparser import ConfigParser
from os import walk
from datetime import datetime
from gamelist.gamelist import RPGameList, GLBrowser, RPGame
from shutil import copyfile
###############################################################################
LOG_FILE = "gltool.log"
DEFAULT_GAMELIST_FILE_NAME = 'new_gamelist.xml'
UseConsoleOut = False
ROOT_NAME = 'gameList'
###############################################################################


class GLHandler:
    '''
    Handler to execute actions on gamelists objects
    '''

    def __init__(self, gamelists=[]):
        '''
        '''
        self.gamelists = gamelists

    def mergeLeft(self):
        '''
        Merge lists to the left most one
        '''
        for l in self.gamelists:
            self.gamelists[0].merge(l)  # TODO

    def mergeRight(self):
        '''
        Merge lists to the right most one
        '''


def log(msg, ERROR=False):
    '''
    log info from program actions
    '''
    with open(LOG_FILE, "a") as f:
        f.write("{}{}\n".format("ERROR: " if ERROR else "", msg))
    if not UseConsoleOut:
        print(msg)


def out_gl_file_name(name=None):
    '''
    return a name for result output file
    '''
    if name:
        return name + '.new'
    else:
        return DEFAULT_GAMELIST_FILE_NAME


def create_file_bak(fpath):
    '''
    create file backup before write
    '''
    fnewpathExt = datetime.now().strftime('.%d-%m-%y_%H-%M-%S')
    fnewpath = fpath + fnewpathExt
    # copyfile(fpath, fnewpath)
    os.rename(fpath, fnewpath)
    log("+ Saved original file {} to {}".format(fpath, fnewpath))


def print_file(gamelist):
    '''
    print file content on output
    '''
    print(gamelist.to_xml())


def create_file(gamelist, fpath, backup=True):
    '''
    create a new file from gamelist. Backup existing one when backup=True 
    '''
    if backup:
        create_file_bak(fpath)
    gamelist.write(fpath)
    log("+ Wrote gamelist in {}".format(fpath))


def get_image_files_in_tree(dpath):
    '''
    find all image files in specified tree path and return a list
    '''
    flist = []
    for (rep, subreps, files) in walk(dpath):
        flist.extend([os.path.join(rep, f).replace('\\', '/')
                     for f in files if f.endswith('.png')])
    return flist


def get_image_files_in_tree_as_map(dpath: str):
    '''
    find all image files in specified tree path and return a map
    '''
    flist: Map[str, str] = {}
    for (rep, subreps, files) in walk(dpath):
        flist.update({f[:-4]: os.path.join(rep, f).replace('\\', '/') #type: ignore
                     for f in files if f.endswith('.png')}) 
    return flist


def complete_empty_image_path(fpath, gamelist=None, repair=False):
    '''
    fix empty paths from images in gamelist
    '''
    log("+ Complete missing game images on {}".format(fpath))
    # get image paths from disk
    # FIXME: image path should be relative to game path: not the case here,
    # we get a full path from search dir
    dpath = os.path.dirname(fpath) or '.'
    prefixLen = 0 if dpath == '.' or dpath == './' else len(dpath) + 1
    img_dic = get_image_files_in_tree_as_map(dpath)
    # get game list with empty images
    gl: RPGameList = gamelist or RPGameList.from_path(fpath)
    # complete game list with found images
    for g in GLBrowser(gl).get_empty_image_games():
        log('Missing image game: {}'.format(g.name()))
        if g.name() in img_dic:
            imagePath = img_dic[g.name()][prefixLen:] #type: ignore
            log('Found image game: {} -> {}'.format(g.name(), imagePath))
            g.image(imagePath)
    return gl


def count_entry(target):
    '''
    Count number of specified entry in gamelist
    '''
    # TODO
    log('-> TODO')


def list_target(fpath, target):
    '''
    list entries from specified 'target' value.

    * image : list all images
    * games : list all game names with path
    * folder: list all folders
    * empty_image: list all specified games without images
    '''
    gl = GLBrowser(RPGameList.from_path(fpath))
    if target == 'image':
        print("\n".join([i for i in gl.get_game_images()]))
    elif target == 'game':
        print(''.join(["{}\n\t{}/{} '{}'\n".format(g.name(),
              g.region(), g.genre(), g.path()) for g in gl.get_games()]))
    elif target == 'folder':
        print(''.join(["{}\n\t'{}' '{}'\n".format(
            g.name(), g.thumbnail(), g.path()) for g in gl.get_folders()]))
    elif target == 'empty_image':
        print("\n".join(["{}: {}".format(g.name(), g.path())
              for g in gl.get_empty_image_games()]))
    else:
        log("Unkown type: {}".format(target), ERROR=True)


def merge_gamelist(glpaths: List[str], keep_doublons=False):
    '''
    merge many gamelist in one. 
    create gamelist objects from param paths and return a new gamelist object
    '''
    log("+ Merging gamelist(s) {}".format(glpaths[:0]))
    root = ET.Element(ROOT_NAME)
    gdic: Map[str, RPGame] = {}
    # g_dic.append({k,v for })#TODO
    for glpath in glpaths:
        for f in RPGameList.from_path(glpath).get_folders():
            gdic[f.path()] = f #type: ignore
        for g in RPGameList.from_path(glpath).get_games():
            gdic[g.path()] = g #type: ignore

    for k, v in gdic.items():
        # if not keep_doublons and RPGameList.from_path(glpath).get_games_by_id(v.id()):
        root.append(v.el)

    return RPGameList(root)


def fix_missing_games(glpath: str):
    '''
    test missing rom's game entries in a gamelist and purge it from them
    '''
    log("+ Check missing game paths on {}".format(glpath))
    pathdir = os.path.dirname(glpath)
    root = ET.Element(ROOT_NAME)
    gl = RPGameList.from_path(glpath)
    glg = gl.get_games()
    #
    for g in glg:
        gpath = os.path.join(pathdir, g.path() or '')
        if not os.path.exists(gpath):
            log("Missing ROM file for game {}. Tested: [{}], Declared: [{}]".format(
                g.name(), gpath, g.path()))
            g.delete()
    #
    return gl


###############################################################################
def main():
    global UseConsoleOut
    parser = argparse.ArgumentParser(
        description='Helpful tool for managing and cleaning gamelist.xml file(s)')
    parser.add_argument('--check', help='clear specified element',
                        type=str, choices=['game', 'title', 'image'], default='')
    parser.add_argument('--clear', help='clear specified element',
                        type=str, choices=['game', 'title', 'image'], default='')
    parser.add_argument(
        '--delete', help='delete game(s) that match selector', type=str)
    parser.add_argument('-l', '--list', help='list the element(s) matching selector',
                        type=str, choices=['game', 'image', 'folder', 'empty_image'])
    parser.add_argument(
        '--count', help='count the number of occurences', type=str, default='', nargs='?')
    parser.add_argument('--repair', help='fix paths issue for games',
                        type=str, choices=['game', 'image', 'all'], nargs='+', default='')
    parser.add_argument('--merge', help='merge gamelists',
                        action='store_true', default=False)
    parser.add_argument('-o', '--console', help='Output result on console (no disk write)',
                        action='store_true', default=False)
    # parser.add_argument('target', help='affect the specified element', choices=['game', 'description', 'title', 'image', 'empty_image', 'folder'])
    parser.add_argument('-f', '--files', dest='gamelist',
                        help='a list of gamelist.xml(s) path(s)', default='gamelist.xml', nargs='*')
    args = parser.parse_args()
    #
    for gl in args.gamelist:
        if not os.path.exists(gl):
            raise Exception('Unknown path {}'.format(gl))

    glpaths = args.gamelist
    UseConsoleOut = args.console or False
    if args.list:
        list_target(glpaths[0], args.list)
    if args.count:
        count_entry(args.count)
    if args.repair or args.check:
        gl = None
        lookup_type = args.repair or args.check
        # loop gamelist file(s)
        for fpath in glpaths:
            if any(item in lookup_type for item in ['game', 'all']):
                gl = fix_missing_games(fpath)
            elif any(item in lookup_type for item in ['image', 'all']):
                gl = complete_empty_image_path(
                    fpath, repair=args.repair is not None)
        # repair only
        if args.repair:
            if UseConsoleOut:
                print_file(gl)
            else:  # write output new file
                create_file(gl, glpaths[0])
    if args.merge:
        gl = merge_gamelist(args.gamelist, UseConsoleOut)
        if UseConsoleOut:
            print_file(gl)
        else:
            gl.write(out_gl_file_name())


###
if __name__ == "__main__":
    main()
