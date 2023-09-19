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
    amenity_ids = []
    reviews = relationship("Review", backref=backref(
        "place", cascade="all, delete"))
    # amenities = relationship(
    #     "Amenity", secondary=place_amenity,
    #     viewonly=False
    # )

    @property
    def reviews(self):
        """
        getter attribute reviews that
        returns the list of Review instances
        """
        return self.reviews

    if getenv("HBNB_TYPE_STORAGE") == "db":
        amenities = relationship(
            "Amenity",
            secondary=place_amenity,
            # back_populates="places_amenities",
            viewonly=False
        )
    # else:

    @property
    def amenities(self):
        """
        getter attribute that returns the list of Amenity instances
        based on the attribute amenity_ids
        """
        from models.__init__ import storage
        from models.amenity import Amenity

        avail_amenities = storage.all(Amenity)
        print("getter method called")
        print("first print : {}".format(avail_amenities))
        result = []
        # for amenity in avail_amenities.values():
        #     if amenity.id in self.amenity_ids:
        #         result.append(amenity)
        # return result
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
        # from models.__init__ import storage
        from models.amenity import Amenity
        print("amenity setter method called")
        if obj and isinstance(Amenity):
            self.amenity_ids.append(obj.id)
