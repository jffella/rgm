# Recalbox Gamelist Manager

## Goal

This project aims at allowing an easier management of gamelist.xml files per hardware configuration in Recalbox.
I was no satisfied by scrapers management of rom files, as there was always missing pictures or duplicate rom entries in game menus. So I decided to create my own manager for Recalbox game lists. Here it is, in fully python.
At term, this project should be available in both CLI and GUI.

## Use

The project requires a version of python superior or equal to python 3.8 at least.

### Display help and General Usage

```shell
python gltool.py --help

usage: gltool.py [-h] [--check {game,title,image}] [--delete DELETE] [-l {game,image,folder,empty_image}] [--count [COUNT]]
                 [--repair {game,image,all} [{game,image,all} ...]] [--merge] [-o] [-v] [-f [GAMELIST [GAMELIST ...]]]

Helpful tool for managing and cleaning gamelist.xml file(s)

optional arguments:
  -h, --help            show this help message and exit
  --check {game,title,image}
                        check specified element
  --delete DELETE       delete game(s) that match regular expression
  -l {game,image,folder,empty_image}, --list {game,image,folder,empty_image}
                        list the element(s) matching selector
  --count [COUNT]       count the number of occurences
  --repair {game,image,all} [{game,image,all} ...]
                        fix paths issue for games
  --merge               merge gamelists
  -o, --console         Output result on console (no disk write)
  -v, --verbose         Output logs on console (no disk write)
  -f [GAMELIST [GAMELIST ...]], --files [GAMELIST [GAMELIST ...]]
                        a list of gamelist.xml(s) path(s)
```

### Manage gamelists

#### Check invalid games paths

```shell
python gltool.py --check game -f pathto/gamelist.xml
```

#### Check invalid images paths

```shell
python gltool.py --check image -f pathto/gamelist.xml
```

#### Merge gamelists and remove doublons (game id match)

```shell
python gltool.py --merge -f path_1/gamelist.xml path_2/gamelist.xml
```

#### Delete game

Delete all matching games

```shell
python gltool.py --delete 'Streets of Rage [1-3]?' -f pathto/gamelist.xml
```

### Repair gamelists

#### Automaticaly detect missing images and fix 

```shell
python gltool.py --repair image -f pathto/gamelist.xml
```

#### Automatically detect missing rom files and remove

```shell
python gltool.py --repair game -f pathto/gamelist.xml
```

### Manage Favorites

#### Export Favorites

```shell
python gltool.py --export-favorites -f pathto/gamelist.xml
```

#### Tag with Favorites

```shell
python gltool.py --import-favorites pathto/favorites.txt -f pathto/gamelist.xml
```
