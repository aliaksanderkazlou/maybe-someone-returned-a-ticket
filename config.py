import configparser

__config = configparser.ConfigParser()
config_section = "main"
__config.read("settings.ini")

config = __config[config_section]
