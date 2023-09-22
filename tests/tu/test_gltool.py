import pytest
from gltool import *

def test_get_image_files_in_tree():
    imgs = get_image_files_in_tree('tests/resources')
    assert len(imgs) != 0
    for i in imgs:
        assert i[-4:] == '.png' or i[-4:] == '.jpg'