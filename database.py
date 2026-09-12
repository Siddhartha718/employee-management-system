# =========================
# IMPORTS
# =========================

import mysql.connector
import os
from dotenv import load_dotenv


# =========================
# LOAD ENVIRONMENT VARIABLES
# =========================

load_dotenv()


# =========================
# DATABASE CONNECTION
# =========================

def connect_database():

    # Connect to MySQL database
    connection = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

    # Return the database connection
    return connection