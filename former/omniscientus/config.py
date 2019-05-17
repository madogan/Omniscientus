class Config:
    """
    Common configurations
    """
    SECRET_KEY = 'ahalirsin'
    
class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True
    HOST = '0.0.0.0'


class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
