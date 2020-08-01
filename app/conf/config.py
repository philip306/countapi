from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "CountAPI"
    ttlsetting: int = 100000
    redishost: str = 'redis'
    port: int = 6379
    db: int = 0
    redispass: str = ""

settings = Settings()