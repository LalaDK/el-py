import configparser

config = configparser.ConfigParser()
config.read('credentials.ini')


def email():
    return config['CREDENTIALS']['Email']


def password():
    return config['CREDENTIALS']['Password']


def aftalenr():
    return config['CREDENTIALS']['Aftalenr']
