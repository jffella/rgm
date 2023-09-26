import xml.etree.ElementTree as ET
# from lxml import etree as ET
###############################################################################


def xml_to_string(xelem):
    '''
    transform an XMLElement to a string and return it
    '''
#    return ET.tostring(xelem, pretty_print=True, xml_declaration=True, encoding='unicode')
    return ET.tostring(xelem, encoding='unicode')
###############################################################################


class RPGameList:
    '''
    Gamelist management object. 
    The gamelist.xml file for a system defines metadata for a system's games, 
    such as a name, image (like a screenshot or box art), description, release date, and rating.
    An example gamelist.xml:

    <gameList>
        <game>
            <path>/home/pi/ROMs/nes/mm2.nes</path>
            <name>Mega Man 2</name>
            <desc>Mega Man 2 is a classic NES game ...</desc>
            <image>~/.es/media/nes/Mega Man 2-image.png</image>
        </game>
    </gameList>
    '''
    @staticmethod
    def from_path(fpath):
        '''
        return RPGamelist object from str path
        '''
        tree = ET.parse(fpath)
        return RPGameList(tree.getroot(), tree)

    def __init__(self, root, tree=None):
        '''
        construct gamelist from XML Element
        '''
        self.root = root  # Element object
        self.tree = tree  # ElementTree object

    def get_games(self, regex='./game'):
        '''
        return games list found in XML gamelist
        '''
        return [RPGame(g, self) for g in self.root.findall(regex)]

    def get_game_images(self, regex='./game/image'):
        '''
        return game images list found in XML gamelist
        '''
        return [str(g.text) for g in self.root.findall(regex)]

    def get_folders(self, regex='./folder'):
        '''
        return game folders found in XML gamelist
        '''
        return [RPFolder(f, self) for f in self.root.findall(regex)]

    def to_xml(self):
        '''
        transform gamelist to XML string
        '''
        return xml_to_string(self.root)

    def __str__(self):
        '''
        transform gamelist to XML string
        '''
        return self.to_xml()

    def write(self, fpath):
        '''
        transform gamelist to XML string and write it in file
        '''
        with open(fpath, 'w', newline='\n') as f:
            f.write(self.to_xml())

    def delete(self, game):
        self.root.remove(game)


class RPElem:
    '''
    base element accessor for game item container. Encapsulates the XML Element
    '''

    def __init__(self, elem, gamelist: RPGameList):
        self.gl: RPGameList = gamelist
        self.el = elem
        self.trash = False

    def get_el_text(self, name):
        return self.el.find(name).text if self.el.find(name) != None else None

    def set_el_text(self, name, newval):
        new_el = ET.SubElement(self.el, name) if self.el.find(
            name) == None else self.el.find(name)
        new_el.text = newval

    def get_set_el_text(self, name, newval):
        if newval:
            self.set_el_text(name, newval)
        return self.get_el_text(name)

    def get_el_attrib(self, name):
        return self.el.attrib[name]

    def set_el_attrib(self, name, newval):
        self.el.set(name, newval)

    def get_set_el_attrib(self, name, newval):
        if newval:
            self.set_el_attrib(name, newval)
        return self.get_el_attrib(name)

    def name(self, val=None):
        if val:
            self.set_el_text('name', val)
        return self.get_el_text('name')

    def image(self, val=None):
        if val:
            self.set_el_text('image', val)
        return self.get_el_text('image')

    def path(self, val=None):
        if val:
            self.set_el_text('path', val)
        return self.get_el_text('path')

    def desc(self, val=None):
        if val:
            self.set_el_text('desc', val)
        return self.get_el_text('desc')

    def thumbnail(self, val=None):
        if val:
            self.set_el_text('thumbnail', val)
        return self.get_el_text('thumbnail')

    def to_xml(self):
        return xml_to_string(self.el)

    def delete(self):
        self.gl.delete(self.el)

    def __str__(self):
        return self.to_xml()


class RPFolder(RPElem):
    '''
    <folder>
    '''


class RPGame(RPElem):
    '''
    <game>
    '''

    def genre(self):
        '''
        get game genre <genre>
        '''
        return self.get_el_text('genre')

    def genreid(self):
        '''
        get game genreid <genreid>
        '''
        return self.get_el_text('genreid')

    def region(self):
        '''
        get game region <region>
        '''
        return self.get_el_text('region')

    def romtype(self):
        '''
        get game romtype <romtype>
        '''
        return self.get_el_text('romtype')

    def players(self):
        '''
        get game nb of players <players>
        '''
        return self.get_el_text('players')

    def publisher(self):
        '''
        get game publisher <publisher>
        '''
        return self.get_el_text('publisher')

    def developer(self):
        '''
        get game developer <developer>
        '''
        return self.get_el_text('developer')

    def releasedate(self):
        '''
        get game releasedate <releasedate>
        '''
        return self.get_el_text('releasedate')

    def rating(self):
        '''
        get game rating <rating>
        '''
        return self.get_el_text('rating')

    def hash(self):
        '''
        get game hash <hash>
        '''
        return self.get_el_text('hash')

    def hidden(self, val=None):
        '''
        get hidden games (hidden attribute)
        '''
        return self.get_set_el_attrib('hidden', val)

    def is_hidden(self):
        '''
        tell game is hidden
        '''
        return self.hidden() == 'true'

    def id(self, val=None):
        '''
        get game id (id attribute)
        '''
        return self.get_set_el_attrib('id', val)

    def source(self, val=None):
        '''
        get game info source
        '''
        return self.get_set_el_attrib('source', val)

    def is_empty_info(self):
        '''
        tell game info (image/desc) is empty
        '''
        return self.image() and self.desc()


class GLBrowser:
    '''
    allows RPGameList browsing
    '''

    def __init__(self, gamelist: RPGameList):
        '''
        create from RPGamelist
        '''
        self.gl: RPGameList = gamelist

    def get_game_images(self):
        '''
        get game images from gamelist
        '''
        return [g for g in self.gl.get_game_images()]

    def get_empty_image_games(self):
        '''
        get only images with an empty path from gamelist
        '''
        return [g for g in self.gl.get_games() if not g.image()]

    def get_empty_desc_games(self):
        '''
        get only games with an empty description
        '''
        return [g for g in self.gl.get_games() if not g.desc()]

    def get_hidden_games(self):
        '''
        get games with hidden attribute
        '''
        return self.gl.get_games('./game/[@hidden="true"]')

    def get_folders(self):
        '''
        get game folders from gamelist
        '''
        return [g for g in self.gl.get_folders()]

    def get_games(self):
        '''
        get all games in gamelist
        '''
        return [g for g in self.gl.get_games()]

    def get_games_by_id(self, id: str):
        '''
        get games matching specified id
        '''
        return self.gl.get_games('./game/[@id="{}"]'.format(id))
