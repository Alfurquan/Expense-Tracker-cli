"""Database module for the app."""
# expense/db.py

import configparser
import json
from pathlib import Path

from . import DB_READ_ERROR, DB_WRITE_ERROR, SUCCESS


DEFAULT_DB_FILE_PATH = Path.home().joinpath(
    "." + Path.home().stem + "_expense.json"
)

class Database:
    def get_database_path(self,config_file: Path) -> Path:
        """
        Return the current path to the database.
        """
        config_parser = configparser.ConfigParser()
        config_parser.read(config_file)
        return Path(config_parser["General"]["database"])

    def init_database(self, db_path: Path) -> int:
        """
        Create the expense database.
        """
        try:
            db_path.write_text("[]") 
            return SUCCESS
        except OSError:
            return DB_WRITE_ERROR
        
    def read_database(self, db_path: Path) -> str:
        """
        Read the database at the path db_path.
        """
        try:
            with db_path.open("r") as db:
                return db.read()
        except OSError:
            raise OSError
        
    def write_database(self, db_path: Path, data: dict) -> int:
        """
        Write the data to the database at the path db_path.
        """
        try:
            with db_path.open("w") as db:
                json.dump(data, db, indent=4)
            return SUCCESS
        except OSError:
            raise OSError