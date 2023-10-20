#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Column, String, DateTime, ForeignKey
from datetime import datetime

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel"""
        if kwargs:
            for key, val in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    if val is not None:
                        val = datetime.strptime(val,
                                                '%Y-%m-%dT%H:%M:%S.%f')
                if key != '__class__':
                    if hasattr(self, key):
                        setattr(self, key, val)
                    else:
                        raise KeyError
            if 'id' not in kwargs:
                setattr(self, 'id', str(uuid.uuid4()))
            if 'created_at' not in kwargs:
                setattr(self, 'created_at', datetime.now())
        else:
            setattr(self, 'id', str(uuid.uuid4()))
            setattr(self, 'created_at', datetime.now())
            setattr(self, 'updated_at', datetime.now())

    def __str__(self):
        """Returns a string representation of the instance"""
        # cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        # clas_dict = self.to_dict()
        # for key, val in clas_dict.items():
        #     if key == 'updated_at' or key == 'created_at':
        #         val = datetime.strptime(val,
        #                                 '%Y-%m-%dT%H:%M:%S.%f')
        #     clas_dict[key] = val
        # return '[{}] ({}) {}'.format(cls, self.id, clas_dict)
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.strftime(
            '%Y-%m-%dT%H:%M:%S.%f')
        dictionary['updated_at'] = self.updated_at.strftime(
            '%Y-%m-%dT%H:%M:%S.%f')
        # dictionary['created_at'] = self.created_at.isoformat()
        # dictionary['updated_at'] = self.updated_at.isoformat()

        # remove _sa_instance_state
        if "_sa_instance_state" in dictionary.keys():
            dictionary.pop("_sa_instance_state", None)

        return dictionary

    def delete(self):
        """
        delete the current instance from the storage (models.storage)
        """
        from models import storage
        storage.delete(self)
