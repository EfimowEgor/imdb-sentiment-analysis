from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    base_path: str
    chart_path: str
    data_path: str
    reviews_count: int

    class Config:
        env_file = "../.env"
        env_prefix = "PRS_"
        extra = "allow"