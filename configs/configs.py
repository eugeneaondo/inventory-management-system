class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Development(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = 'postgres://postgres:postgres@127.0.0.1:5432/ecommerce'
