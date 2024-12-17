from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    """
    Base configuration class with shared settings.
    """
    model_config = SettingsConfigDict(env_file='settings.env')


class Config(BaseConfig):
    """
    Configuration for the news service.
    """
    kafka_broker_address: str
    kafka_topic: str
    polling_interval_sec: int = 10  # Default value simplified


class CryptopanicConfig(BaseConfig):
    """
    Configuration for the Cryptopanic API.
    """
    model_config = SettingsConfigDict(env_file='cryptopanic_credentials.env')
    api_key: str


config = Config()
cryptopanic_config = CryptopanicConfig()
