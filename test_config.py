from configparser import ConfigParser

def read_sections(config):
    system = config["System"]
    window = config["Window"]
    fpaths = config["Files Path"]
    print(not system.getboolean("console"))
    print(window.getfloat("zoomfactor") * 4)
    print(window.get("not existing", "default"))
    print(window.get("Compression", False))
    print(window.get("CompressionLevel", 42))

###############################################################################
def main ():
    config = ConfigParser()
    config['DEFAULT'] = {'Compression': True, 'CompressionLevel' : 9}
    config.read("./config.ini")
    for i in config.sections():
        print("[{}]".format(i))
        for k in config[i]:
            print("\t{} \t= {}".format(k, config[i][k]))
    #
    read_sections(config)

###
if __name__ == "__main__":
    main()
