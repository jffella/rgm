# Recalbox Gamelist Manager

## Goal

This project aims at allowing an easier management of gamelist.xml files per hardware configuration in Recalbox.
I was no satisfied by scrapers management of rom files, as there was always missing pictures or duplicate rom entries in game menus. So I decided to create my own manager for Recalbox game lists. Here it is, in fully python.
At term, this project should be available in both CLI and GUI.

## Use

### Display help and General Usage

```shell
python3 gltool.py --help
```
### Check gamelists

#### Check invalid games paths

```shell
python3 gltool.py --check game -f pathto/gamelist.xml
```

#### Check invalid images paths

```shell
python3 gltool.py --check image -f pathto/gamelist.xml
```

### Repair gamelists

#### Automaticaly detect missing images and fix 

```shell
python3 gltool.py --repair image -f pathto/gamelist.xml
```
