DB_NAME = "clean_data"
DB_USERNAME = "root"
DB_PASSWORD = ""


class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False
    IMAGE_UPLOADS = "./app/static/uploads"
    EXCEL_UPLOADS = "./app/static/uploads"

    SESSION_COOKIE_SECURE = False


class DevelopmentConfig(Config):
    DEBUG = True

    IMAGE_UPLOADS = "./app/static/uploads"
    EXCEL_UPLOADS = "./app/static/uploads"

    SESSION_COOKIE_SECURE = False
    TEMPLATES_AUTO_RELOAD = True


class TestingConfig(Config):
    TESTING = True

    DB_NAME = "clean_data"
    DB_USERNAME = "root"
    DB_PASSWORD = ""

    IMAGE_UPLOADS = "./app/static/uploads"
    EXCEL_UPLOADS = "./app/static/uploads"

    SESSION_COOKIE_SECURE = False
