# utils.py

# Import the session object from the flask module. This object allows you to store information specific to a user from one request to the next.

from flask import session
from urllib.parse import urlparse
from .models import FileRecord
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


engine = create_engine('postgresql://user:password@localhost/dbname')
Session = sessionmaker(bind=engine)

# Define a function to store file information in the user's session.
def store_file_info_in_session(file_info):
    # Store the file information in the session under the key 'file_info'.
    session['file_info'] = file_info

# Define a function to get file information from the user's session.
def get_file_info_from_session():
    # Return the file information stored in the session under the key 'file_info'. If no such information exists, return None.
    return session.get('file_info')

def get_file_record(unique_id):
    session = Session()
    file_record = None
    try:
        file_record = session.query(FileRecord).filter(FileRecord.unique_identifier == unique_id).first()
    except Exception as e:
        print(f"Error getting file record: {e}")
    finally:
        session.close()
    return file_record


def format_sqlalchemy_url_for_psycopg2(sqlalchemy_url):
    result = urlparse(sqlalchemy_url)
    dbname = result.path[1:]  # remove leading slash
    user = result.username
    password = result.password
    host = result.hostname
    port = result.port
    return f"dbname={dbname} user={user} password={password} host={host} port={port}"