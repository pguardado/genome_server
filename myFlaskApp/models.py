# Import the db object from the db module in the current package. This object represents the database.

from .db import db

# Import the os module. This module provides a way of using operating system dependent functionality.
import os

# FileRecord is a class that inherits from db.Model, representing a table in the database.
class FileRecord(db.Model):
    # id is a column of type Integer. It is the primary key of the table.
    id = db.Column(db.Integer, primary_key=True)
    
    # unique_identifier is a column of type String. It cannot be null.
    # This could be used to store a unique identifier for each record.
    unique_identifier = db.Column(db.String, nullable=False)
    
    # filename is a column of type String. It cannot be null.
    # This could be used to store the name of the file associated with each record.
    filename = db.Column(db.String, nullable=False)
    
    # file_path is a column of type String. It cannot be null.
    # This could be used to store the path of the file associated with each record.
    file_path = db.Column(db.String, nullable=False)

    # get_contents is a method that reads the file from the file system and returns its contents.
    def get_contents(self):
        """Read the file from the file system and return its contents."""
        # Check if the file exists in the file system.
        if os.path.exists(self.file_path):
            # If it does, open the file and read its contents.
            with open(self.file_path, 'r') as file:
                return file.read()
        else:
            # If the file does not exist, return None.
            return None