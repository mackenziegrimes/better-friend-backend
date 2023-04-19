from os import getenv

class Config: 
    AUTH_KEY: str
    PORT: str
    DB_HOST: str 
    DB_USER: str 
    DB_PASS: str 
    DB_PORT: str

    # TODO this isn't successfully pulling env vars, why?
    def __init__(self) -> None:
        AUTH_KEY = getenv("AUTH_KEY")
        PORT = getenv("PORT")

        DB_HOST = getenv("DB_HOST")
        DB_USER = getenv("DB_USER")
        DB_PASS = getenv("DB_PASS")
        DB_PORT = getenv("DB_PORT")
