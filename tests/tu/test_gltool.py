import pytest
from gltool import *

def test_get_image_files_in_tree():
    imgs = get_image_files_in_tree('tests/resources')
    assert len(imgs) != 0
    for i in imgs:
        assert i[-4:] == '.png' or i[-4:] == '.jpg'

def test_merge_gamelist_diff():
    gla = ['tests/tu/gamelist-merge1.xml', 'tests/tu/gamelist-merge2.xml']
    gl_mrg = merge_gamelist(gla)
    assert len(gl_mrg.get_games()) == 2

def test_merge_gamelist_same():
    gla = ['tests/tu/gamelist-merge1.xml', 'tests/tu/gamelist-merge1.xml']
    gl_mrg = merge_gamelist(gla)
    assert len(gl_mrg.get_games()) == 1
    #FIXME
    #gl_mrg = merge_gamelist(gla, keep_doublons=True)
    #assert len(gl_mrg.get_games()) == 2

def test_fix_missing_games():
    gl = RPGameList.from_path('tests/tu/gamelist-purge.xml')
    assert len(gl.get_games()) == 2
    gl_purged = fix_missing_games('tests/tu/gamelist-purge.xml')
    assert len(gl_purged.get_games()) == 1
