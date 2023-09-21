import xml.etree.ElementTree as ET
#from lxml import etree as ET
###############################################################################
def xml_to_string(xelem):
#    return ET.tostring(xelem, pretty_print=True, xml_declaration=True, encoding='unicode')
    return ET.tostring(xelem, encoding='unicode')
###############################################################################
class RPGameList:
    '''
    gamelist management
    '''
    @staticmethod
    def from_path(fpath):
        '''
        return RPGamelist object from str path
        '''
        tree = ET.parse(fpath)
        return RPGameList(tree.getroot(), tree)
    def __init__(self, root, tree = None):
        self.root = root # Element object
        self.tree = tree # ElementTree object
    def get_games(self, regex='./game'):
        return [RPGame(g, self) for g in self.root.findall(regex)]
    def get_game_images(self, regex='./game/image'):
        return [str(g.text) for g in self.root.findall(regex)]
    def get_folders(self, regex='./folder'):
        return [RPFolder(f, self) for f in self.root.findall(regex)]
    def to_xml(self):
        return xml_to_string(self.root)
    def __str__(self):
        return self.to_xml()
    def write(self, fpath):
        with open(fpath, 'w', newline='\n') as f:
            f.write(self.to_xml())
    def delete(self, game):
        self.root.remove(game)

class RPElem:
    '''
    base element accessor for game item container. Encapsulates the XML Element
    '''
    def __init__(self, elem, gamelist):
        self.gl = gamelist
        self.el = elem
        self.trash = False
    def get_el_text(self, name):
        return self.el.find(name).text if self.el.find(name) != None else None
    def set_el_text(self, name, newval):
        new_el = ET.SubElement(self.el, name) if self.el.find(name) == None else self.el.find(name)
        new_el.text = newval
    def get_set_el_text(self, name, newval):
        if newval: self.set_el_text(name, newval)
        return self.get_el_text(name)
    def get_el_attrib(self, name):
        return self.el.attrib[name]
    def set_el_attrib(self, name, newval):
        self.el.set(name, newval)
    def get_set_el_attrib(self, name, newval):
        if newval: self.set_el_attrib(name, newval)
        return self.get_el_attrib(name)
    def name(self, val=None):
        if val: self.set_el_text('name', val)
        return self.get_el_text('name')
    def image(self, val=None):
        if val: self.set_el_text('image', val)
        return self.get_el_text('image')
    def path(self, val=None):
        if val: self.set_el_text('path', val)
        return self.get_el_text('path')
    def desc(self, val=None):
        if val: self.set_el_text('desc', val)
        return self.get_el_text('desc')
    def to_xml(self):
        return xml_to_string(self.el)
    def delete(self):
        self.gl.delete(self.el)
    def __str__(self):
        return self.to_xml()


class RPGame(RPElem):
    '''
    '''
    def thumbnail(self, val=None):
        if val: self.set_el_text('thumbnail', val)
        return self.get_el_text('thumbnail')
    def genre(self):
        return self.get_el_text('genre')
    def genreid(self):
        return self.get_el_text('genreid')
    def region(self):
        return self.get_el_text('region')
    def romtype(self):
        return self.get_el_text('romtype')
    def players(self):
        return self.get_el_text('players')
    def publisher(self):
        return self.get_el_text('publisher')
    def developer(self):
        return self.get_el_text('developer')
    def releasedate(self):
        return self.get_el_text('releasedate')
    def rating(self):
        return self.get_el_text('rating')
    def hash(self):
        return self.get_el_text('hash')
    def hidden(self, val=None):
        return self.get_set_el_attrib('hidden', val)
    def is_hidden(self):
        return self.hidden() == 'true'
    def id(self, val=None):
        return self.get_set_el_attrib('id', val)
    def source(self, val=None):
        return self.get_set_el_attrib('source', val)
    def is_empty_info(self):
        return self.image() and self.desc()


class RPFolder(RPElem):
    '''
    '''
    pass


class GLBrowser:
    '''
    allows RPGameList browsing
    '''
    def __init__(self, gamelist):
        self.gl = gamelist
    def get_game_images(self):
        return [g for g in self.gl.get_game_images()]
    def get_empty_image_games(self):
        return [g for g in self.gl.get_games() if not g.image()]
    def get_empty_desc_games(self):
        return [g for g in self.gl.get_games() if not g.desc()]
    def get_hidden_games(self):
        return self.gl.get_games('./game/[@hidden="true"]')
    def get_folders(self):
        return [g for g in self.gl.get_folders()]
    def get_games(self):
        return [g for g in self.gl.get_games()]
