
from unittest import TestCase
from app import app
from models import db, User


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False



db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    
    def setUp(self):
        """Clean up any existing Users in the db."""
        
        User.query.delete()
    
    def tearDown(self):
        """Clean up any additions/changes made in the db."""
        
        db.session.rollback()
        
    def test_adding_user(self):
        """Tests if adding user to db works."""
        
        user = User(first_name='Frank', last_name='Ocean', img_url='https://a.espncdn.com/photo/2015/1212/r35307_1296x729_16-9.jpg')

        db.session.add(user)
        db.session.commit()
        
        singer = User.query.filter_by(last_name='Ocean').first()
        self.assertEquals(singer, [user])
    
    # def greet(self):
    #     return f"Hi, my name is {self.name} and i'm a {self.species}!"
    
    # def feed(self, amt=20):
    #     """Update hunger based off of amt"""
        
    #     self.hunger -= amt
    #     self.hunger = max(self.hunger, 0)
    
    # to run this class use the following
    # ipython3
    # %run app.py
    # db.create_all()
    
    # if you add or update the table and then want to update it,
    # you need to go to the Postgres Shell and run DROP table_name,
    # then re run db.create_all()
    
    # Then make sure you import the class name in your app.py file
    
    # To create a instance of this class, type this in ipython, do the follwoing:
    # stevie = Pet(name="Stevie Chicks", species="Chicken", hunger=13)
    
    # then you can use, stevie.name, stevie.hunger, stevie.SMTPRecipientsRefused
    
    # then to sync all of the pets youve created once your done, do the following:
    # db.session.add(stevie)
    # db.session.commit()
    
    # to create a lot of instances at once, you can do the following using sip:
    # names = ['Sushi', 'scout', 'piggie', 'carrot face']
    # species = ['pig', 'cat', 'bunny', 'bunny']
    # pets = [Pet(name=n, species=s) for n,s in zip(names, species)]
    # db.session.add_all(pets) *add_all needs to be ZipFile The class for reading and writing ZIP files.  See section 
    # db.session.commit()
