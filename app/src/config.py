from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_path: str
    model_name: str
    data_path: str

    class Config:
        env_file = "../.env"
        env_prefix = "MDL_"
        extra = "allow"