from app import app
from sqlalchemy import (
    create_engine,
    MetaData,
    text,
    Table,
    Column,
    String,
    insert,
    select,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.base import Connection
from sqlalchemy.exc import OperationalError
from ordereduuid import OrderedUUID

import config

# from app.models import UserModel, ActivityModel
from werkzeug.security import generate_password_hash, check_password_hash

# Membuat koneksi ke database
engine = create_engine(f"mysql://{config.DB_USERNAME}:{config.DB_PASSWORD}@localhost/")
Session = sessionmaker(bind=engine)
db_mysql = Session()

# Membuat objek metadata
metadata = MetaData()


def ExecuteOnce():
    # Membuat database 'clean_data' jika belum ada
    create_database_query = text(f"CREATE DATABASE IF NOT EXISTS {config.DB_NAME}")
    db_mysql.execute(create_database_query)

    # Membuat tabel 'users' jika belum ada
    create_users_table_query = text(
        f"""
        USE {config.DB_NAME};
    CREATE TABLE IF NOT EXISTS {config.DB_NAME}.users (
        id VARCHAR(255) PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        role VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    );

    """
    )
    db_mysql.execute(create_users_table_query)

    # Membuat tabel 'activities' jika belum ada
    create_activities_table_query = text(
        f"""
    CREATE TABLE IF NOT EXISTS {config.DB_NAME}.activities (
        id VARCHAR(255) PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        description TEXT
    );

    """
    )
    db_mysql.execute(create_activities_table_query)

    # Commit perubahan ke database
    db_mysql.commit()


    
    return db_mysql


try:
    # q = text(f"USE clean_data")
    q = text(f"USE {config.DB_NAME}")
    db_mysql.execute(q)  # Coba gunakan database clean_data
except OperationalError:
    # Jika database clean_data belum ada, maka buat database tersebut
    db_mysql = ExecuteOnce()  # Panggil fungsi ExecuteOnce
