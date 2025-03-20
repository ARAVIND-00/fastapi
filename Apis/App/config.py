from turtle import st
from pydantic_settings import BaseSettings,SettingsConfigDict

model_config = SettingsConfigDict(env_file=".env")

class Setting(BaseSettings):
    database_hostname:str
    database_password:str
    database_port:str
    database_name:str
    database_username:str
    secret_key:str
    algorthm:str
    access_token_expire_minutes:int

  
