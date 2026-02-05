import configparser

def gs(wanted_variable):
    config = configparser.ConfigParser()

    config.read('./config/settings.ini') # Read the .ini file

    if wanted_variable:
        for section in config.sections():
            if config.has_option(section, wanted_variable):
                return config.get(section, wanted_variable)