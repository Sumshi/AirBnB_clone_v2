#!/usr/bin/python3

"""database storage class"""

from sqlalchemy.orm import Session
from sqlalchemy import (create_engine)
import MySQLdb
from os import getenv

class DBStorage:
    """class DBStorage
    args:
    __engine: None
    __session: None
    """
    __engine = None
    __session = None

    def __init__(self):
        """linking to mysql database"""
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        database = getenv("HBNB_MYSQL_DB")
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(user, password, host, database), pool_pre_ping=True)

