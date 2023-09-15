from app.db.mysql import session


def MakeDB():
    # Membuat database 'clean_data' jika belum ada
    session.execute("CREATE DATABASE IF NOT EXISTS clean_data")

    session.execute(
        """
    USE clean_data               
    -- Membuat tabel 'users' jika belum ada
    CREATE TABLE IF NOT EXISTS clean_data.users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        role VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    );

    -- Membuat tabel 'activities' jika belum ada
    CREATE TABLE IF NOT EXISTS clean_data.activities (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        description TEXT,
        FOREIGN KEY (username) REFERENCES users(username)
    );"""
    )
