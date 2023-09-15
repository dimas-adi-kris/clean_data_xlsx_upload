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
from ordereduuid import OrderedUUID
from app.models import UserModel, ActivityModel
from werkzeug.security import generate_password_hash, check_password_hash

# Membuat koneksi ke database
engine = create_engine("mysql://root:@localhost/")
Session = sessionmaker(bind=engine)
session = Session()

# Membuat objek metadata
metadata = MetaData()


def ExecuteOnce():
    # Membuat database 'clean_data' jika belum ada
    create_database_query = text("CREATE DATABASE IF NOT EXISTS clean_data")
    session.execute(create_database_query)

    # Membuat tabel 'users' jika belum ada
    create_users_table_query = text(
        """
        USE clean_data;
    CREATE TABLE IF NOT EXISTS clean_data.users (
        id VARCHAR(255) PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        role VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    );

    """
    )
    session.execute(create_users_table_query)

    # Membuat tabel 'activities' jika belum ada
    create_activities_table_query = text(
        """
    CREATE TABLE IF NOT EXISTS clean_data.activities (
        id VARCHAR(255) PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        description TEXT
    );

    """
    )
    session.execute(create_activities_table_query)

    # Commit perubahan ke database
    session.commit()

    data_activities = ActivityModel.get_all_data()
    data_users = UserModel.get_all_data()

    users = Table(
        "users",
        metadata,
        Column("id", String(255), primary_key=True),
        Column("username", String(255), unique=True, nullable=False),
        Column("role", String(255), nullable=False),
        Column("password", String(255), nullable=False),
        extend_existing=True,  # Add this line
    )
    activities = Table(
        "activities",
        metadata,
        Column("id", String(255), primary_key=True),
        Column("username", String(255)),
        Column("description", String(255)),
        extend_existing=True,  # Add this line
    )

    # Check if data exists in the tables before inserting
    if not session.query(users.select().exists()).scalar():
        for data in data_users:
            id = str(OrderedUUID())  # Make sure OrderedUUID is correctly imported
            username = data["username"]
            password = generate_password_hash("123456")
            role = data["role"]
            stmt = insert(users).values(
                id=id, username=username, role=role, password=password
            )
            session.execute(stmt)

    if not session.query(activities.select().exists()).scalar():
        for data in data_activities:
            id = str(OrderedUUID())  # Make sure OrderedUUID is correctly imported
            username = data["username"]
            description = data["description"]
            stmt = insert(activities).values(
                id=id, username=username, description=description
            )
            session.execute(stmt)

    # Commit the changes
    session.commit()

    # Close the session when done
    session.close()
