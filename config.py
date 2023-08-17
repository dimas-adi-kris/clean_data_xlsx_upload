class Config(object):
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    DEBUG = True

    DB_NAME = "development-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"

    IMAGE_UPLOADS = "./app/static/uploads"
    EXCEL_UPLOADS = "./app/static/uploads"

    SESSION_COOKIE_SECURE = False

class DevelopmentConfig(Config):
    DEBUG = True

    DB_NAME = "development-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"

    IMAGE_UPLOADS = "./app/static/uploads"
    EXCEL_UPLOADS = "./app/static/uploads"

    SESSION_COOKIE_SECURE = False
    TEMPLATES_AUTO_RELOAD = True


class TestingConfig(Config):
    TESTING = True

    DB_NAME = "development-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"

    SESSION_COOKIE_SECURE = False
