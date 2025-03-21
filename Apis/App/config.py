from turtle import st
from pydantic_settings import BaseSettings,SettingsConfigDict


class Setting(BaseSettings):
    database_hostname:str
    database_password:str
    database_port:str
    database_name:str
    database_username:str
    secret_key:str
    algorthm:str
    access_token_expire_minutes:int
    model_config = SettingsConfigDict(env_file=".env",extra="ignore")

settings=Setting()