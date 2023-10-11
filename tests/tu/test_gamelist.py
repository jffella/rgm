import pytest
from gamelist.gamelist import *


@pytest.fixture
def gl1_from_path():
    return RPGameList.from_path('tests/tu/gamelist-one-game.xml')


@pytest.fixture
def gl2_from_path():
    return RPGameList.from_path('tests/tu/gamelist-one-game2.xml')


@pytest.fixture
def glb(gl1_from_path):
    return GLBrowser([gl1_from_path])


@pytest.fixture
def glb2(gl1_from_path, gl2_from_path):
    return GLBrowser([gl1_from_path, gl2_from_path])


def test_from_path():
    gl = RPGameList.from_path('tests/tu/gamelist-one-game.xml')
    assert gl != None and isinstance(gl, RPGameList)
    games = gl.get_games()
    assert len(games) == 1
    ffgame = games[0]
    assert ffgame.name() == 'Final Fight (World)'
    assert ffgame.path() == 'mame/ffight.zip'
    assert ffgame.publisher() == 'Capcom'
    assert ffgame.id() == 'ffight'
    ffgame.id('ffight2')
    assert ffgame.id() == 'ffight2'
    # GLBrowser load test
    glb = GLBrowser.load(['tests/tu/gamelist-one-game.xml', 'tests/tu/gamelist-one-game2.xml'])
    assert len(glb.get_games()) == 2


def test_games(glb, glb2):
    ## one gamelist
    assert len(glb.get_games()) == 1
    assert len(glb.get_hidden_games()) == 0
    assert len(glb.get_game_images()) == 1
    assert glb.get_game_images()[0] == './media/Final Fight (World).jpg'
    ffgames = glb.get_games_by_id('ffight')
    assert len(ffgames) == 1
    assert ffgames[0].name() == 'Final Fight (World)'
    assert len(glb.get_games_by_id('ffight2')) == 0
    # gamelist len test
    assert len(glb.gll[0]) == 1
    ## 2 gamelist
    assert len(glb2.get_games()) == 2
    assert len(glb2.get_hidden_games()) == 0
    assert len(glb2.get_game_images()) == 2
    assert glb2.get_game_images()[1] == './media/fatfury1-image.jpg'
    ffgames = glb2.get_games_by_id('fatfury1')
    assert len(ffgames) == 1
    assert ffgames[0].name() == 'Fatal Fury - King of Fighters / Garou Densetsu - shukumei no tatakai (NGM-033)(NGH-033) '
    assert len(glb2.get_games_by_id('fatfury2')) == 0
    # test favorites
    assert len(glb2.get_favorite_gamelists()) == 1
    assert len(glb2.get_favorite_games()) == 1
    # gamelist len test
    assert len(glb2.gll[0]) == 1
    ## gamelist iterable test
    for gl in glb2.gll:
        for g in gl:
            assert g != None
            assert g.name() != None


def test_folders(glb):
    assert len(glb.get_folders()) == 1
    folder0 = glb.get_folders()[0]
    assert folder0.name() == 'MAME'
    assert folder0.path() == 'mame'
