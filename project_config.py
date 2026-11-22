
from pathlib import Path

import duckdb
import pandas as pd


# ==========================================
# 1. ПУТИ ПРОЕКТА
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent

DATA_DIR = PROJECT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
DB_DIR = DATA_DIR / "database"

REPORTS_DIR = PROJECT_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
DOCS_DIR = PROJECT_DIR / "docs"

DB_PATH = DB_DIR / "steam_analytics.duckdb"


# ==========================================
# 2. ПОДКЛЮЧЕНИЕ К DUCKDB
# ==========================================

def connect_db(read_only=True):
    """
    Открывает существующую базу DuckDB.

    read_only=True:
        только чтение.

    read_only=False:
        чтение и изменение базы.
    """
    if not DB_PATH.is_file():
        raise FileNotFoundError(
            f"База данных не найдена: {DB_PATH}"
        )

    return duckdb.connect(
        database=str(DB_PATH),
        read_only=read_only
    )


# ==========================================
# 3. ЗАГРУЗКА CSV
# ==========================================

def load_csv(filename, folder="raw", **kwargs):
    """
    Загружает CSV в pandas DataFrame.

    folder:
        raw или processed.
    """

    folders = {
        "raw": RAW_DIR,
        "processed": PROCESSED_DIR
    }

    if folder not in folders:
        raise ValueError(
            "folder должен быть raw или processed"
        )

    path = folders[folder] / filename

    if not path.is_file():
        raise FileNotFoundError(
            f"CSV-файл не найден: {path}"
        )

    return pd.read_csv(path, **kwargs)


# ==========================================
# 4. СПИСОК CSV
# ==========================================

def list_csv(folder="raw"):

    folders = {
        "raw": RAW_DIR,
        "processed": PROCESSED_DIR
    }

    if folder not in folders:
        raise ValueError("Неизвестная папка")

    return sorted(f.name for f in folders[folder].glob("*.csv"))


# ==========================================
# 5. СПИСОК ТАБЛИЦ DUCKDB
# ==========================================

def list_tables(con):
    return con.execute("""
        SELECT
            table_schema,
            table_name,
            table_type
        FROM information_schema.tables
        WHERE table_schema NOT IN (
            'information_schema',
            'pg_catalog'
        )
        ORDER BY table_schema, table_name
    """).df()



