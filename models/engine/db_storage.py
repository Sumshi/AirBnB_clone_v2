#!/usr/bin/python3

"""database storage class"""

from sqlalchemy.orm import sessionmaker
from sqlalchemy import (create_engine)
import MySQLdb
from models.base_model import Base
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
        env = getenv("HBNB_ENV")
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(user, password, host, database), pool_pre_ping=True)

        Base.metadata.create_all(self.__engine)
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
        objects = {}
        # create session maker object that binds to the previous db
        Session = sessionmaker(bind=self.__engine)

        # creates a new session
        self.__session = Session()
        
        if (cls is None):
            for items in classes:
                query = self.__session.query(items)
                for obj in query.all():
                    obj_key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                    objects[obj_key] = obj
        else:
            if cls in classes:
                query = self.__session.query(classes[cls])
                for obj in query.all():
                    obj_key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                    objects[obj_key] = obj
        return objects

