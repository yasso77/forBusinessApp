from passlib.hash import bcrypt

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
    
    