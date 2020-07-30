from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "CountAPI"
    ttlsetting: int = 100000
    redishost: str = '192.168.25.12'
    port: int = 6379
    db: int = 0
    redispass: str = ""

settings = Settings()