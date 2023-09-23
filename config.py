class ProductionConfig(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:password1234@bojio-db.c3tfalfhp9o3.ap-southeast-1.rds.amazonaws.com/bojio-db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:j1a2c3k4@localhost/bojio_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
