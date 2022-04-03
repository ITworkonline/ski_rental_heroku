import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    #secret key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'A-VERY-LONG-SECRET-KEY'

    #recaptcha key
    #RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY') or 'A-VERY-LONG-RECAPTCHA-KEY'

    #database initialization
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///'+os.path.join(basedir, 'app.db') # for user info db
    SQLALCHEMY_BINDS = {'ski': 'sqlite:///'+os.path.join(basedir, 'ski.db')} # for ski equipment db


    SQLALCHEMY_TRACK_MODIFICATIONS = False



    #gmail config
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'jiewang0171@gmail.com'
    MAIL_PASSWORD = 'fuwhwhyzgrgvnlwz'
