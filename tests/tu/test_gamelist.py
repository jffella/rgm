import pytest
from gamelist.gamelist import RPGameList, GLBrowser

@pytest.fixture
def gl_from_path():
    return RPGameList.from_path('tests/tu/gamelist-one-game.xml')

@pytest.fixture
def glb(gl_from_path):
    return GLBrowser(gl_from_path)

def test_from_path():
    gl = RPGameList.from_path('tests/tu/gamelist-one-game.xml')
    assert gl != None and isinstance(gl, RPGameList)
    games = gl.get_games()
    assert len(games) == 1
    ffgame = games[0]
    assert ffgame.name() == 'Final Fight (World)'
    assert ffgame.path() == 'mame/ffight.zip'
    assert ffgame.publisher() == 'Capcom'
    assert ffgame.id() == '100'
    ffgame.id('101')
    assert ffgame.id() == '101'

def test_games(glb):
    assert len(glb.get_games()) == 1
    assert len(glb.get_hidden_games()) == 0
    assert len(glb.get_game_images()) == 1
    assert glb.get_game_images()[0] == './media/Final Fight (World).jpg'
    ffgames = glb.get_games_by_id('100')
    assert len(ffgames) == 1
    assert ffgames[0].name() == 'Final Fight (World)'
    assert len(glb.get_games_by_id('101')) == 0

def test_folders(glb):
    assert len(glb.get_folders()) == 1
    folder0 = glb.get_folders()[0]
    assert folder0.name() == 'MAME'
    assert folder0.path() == 'mame'