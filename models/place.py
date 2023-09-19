#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Float, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship, backref
from os import getenv

place_amenity = Table(
    'place_amenity',
    Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'), primary_key=True),
    Column('amenity_id', String(60), ForeignKey(
        'amenities.id'), primary_key=True)
)


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    if getenv("HBNB_TYPE_STORAGE") == "db":
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship("Review", backref=backref(
            "place", cascade="all, delete"))
        amenities = relationship(
            "Amenity",
            secondary=place_amenity,
            back_populates='place_amenities',
            viewonly=False
        )
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """
            getter attribute reviews that
            returns the list of Review instances
            """
            from models import storage, Review
            result = []
            for review in storage.all(Review).values():
                if review.place_id == self.id:
                    result.append(review)
            return result

        @property
        def amenities(self):
            """
            getter attribute that returns the list of Amenity instances
            based on the attribute amenity_ids
            """
            from models import storage, Amenity

            result = []
            for amenity_id in self.amenity_ids:
                key = "Amenity." + amenity_id
                if key in storage.all(Amenity):
                    result.append(storage.all(Amenity)[key])
            return result

        @amenities.setter
        def amenities(self, obj):
            """
            Setter attribute amenities that handles append method
            for adding an Amenity.id to the attribute amenity_ids
            """

            from models.amenity import Amenity
            print("amenity setter method called")
            if obj and isinstance(Amenity):
                self.amenity_ids.append(obj.id)
