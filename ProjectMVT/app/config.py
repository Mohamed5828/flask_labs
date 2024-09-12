class Config:
    @staticmethod
    def init_app():
        pass
class DevelopmentConfig(Config):
    # static attributes
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///project.db"

class ProductionConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://"


config_options = {
    "dev":DevelopmentConfig,
    'prd':ProductionConfig
}