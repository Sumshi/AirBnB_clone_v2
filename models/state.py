#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, backref
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref=backref(
            "state", cascade="all, delete"))
    else:
        name = ""

        @property
        def cities(self):
            """getter attribute that returns a list of city
            instances with state_id equals to the current state.id
            """
            from models import storage
            related_cities = []
            my_cities = storage.all(City)
            for city in my_cities.values():
                if self.id == city.state_id:
                    related_cities.append(city)
            return related_cities
