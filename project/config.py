isTest = False

class ProductionConfig(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:password1234@bojio-db.c3tfalfhp9o3.ap-southeast-1.rds.amazonaws.com/bojio-db'
    SECRET_KEY = 'not really secret'

class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/bojio_db'
    SECRET_KEY = 'not really secret'

class TestConfig(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = 'not really secret'
