from pydantic import BaseSettings

class Settings(BaseSettings):
     database_password: str = 'Nguyen2003'
     database_username: str = "postgres"
     database_name : str = 'fastapi'
     database_port : int = 5433
     host :str = 'localhost'
     secret_key: str = "8tu509ntguitug9tu095ug09urru0934895798t7ygihg9ty85g"


settings = Settings()