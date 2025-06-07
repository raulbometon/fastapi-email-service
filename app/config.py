#config.py

from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_config = ConfigDict(env_file='.env')

    aws_access_key_id: str = Field(..., env="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = Field(..., env="AWS_SECRET_ACCESS_KEY")
    aws_default_region: str = Field(..., env="AWS_DEFAULT_REGION")

    default_from: str = Field(..., env="DEFAULT_FROM")
    default_mailer: str = Field(..., env="DEFAULT_MAILER")
    
    templates_dir: str = Field(..., env="TEMPLATES_DIR")



settings = Settings()