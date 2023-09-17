#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel


class State(BaseModel):
    """ State class """
    name = ""

    def __init__(self, *args, **kwargs):
        """
        Method to initialize the State class instance

        Args:
            args - variable arguments
            kwargs - key word arguments
        """
        super().__init__(*args, **kwargs)
