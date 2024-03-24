"""Top-level package for Expense tracker."""
# expense/__init__.py

__app_name__ = "Expense Tracker"
__version__ = "0.1.0"

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
    JSON_ERROR,
    ID_ERROR,
    ITEM_NOT_FOUND_ERROR,
) = range(8)

ERRORS = {
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error",
    DB_READ_ERROR: "database read error",
    DB_WRITE_ERROR: "database write error",
    ID_ERROR: "expense id error",
    ITEM_NOT_FOUND_ERROR: "item not found error",
}