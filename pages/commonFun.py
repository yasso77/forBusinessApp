import os
from passlib.hash import bcrypt
import uuid
from django.utils.deconstruct import deconstructible
@deconstructible
class PathAndRename:
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        # Split the file name and extension
        name, ext = os.path.splitext(filename)
        # Generate a unique suffix with uuid
        unique_suffix = uuid.uuid4().hex[:7]        
        # Combine the original name with the unique suffix and extension
        unique_filename = f"{name}_{unique_suffix}{ext}"
        # Return the full path to the file
        return os.path.join(self.path, unique_filename)

    
class CommonFunctions():
    def hash_password(password: str) -> str:
        return bcrypt.hash(password)


    def verify_password(password: str, password_hash: str):
        return bcrypt.verify(password, password_hash)

    def countryList():
        Country_CHOICES = [
            ('Saudia Arabia', 'Saudia Arabia'),
            ('Qatar', 'Qatar'),
            ('Oman', 'Oman'),
            ('United Arab Emirates', 'United Arab Emirates'),
            ('Bahrian', 'Bahrian'),
            ('Kuwait', 'Kuwait'),
            ('Egypt', 'Egypt'),
            ]
        
        return Country_CHOICES
    
    def genderList():
        GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ]
        return GENDER_CHOICES
        
    def contractTypes():
       Contract_types=[
        ('Freelance','Freelance'),
        ('Full Time', 'Full Time'),
        ('Part Time','Part Time'),
        ('Temporary', 'Temporary'),
         ]
       return Contract_types
    
    