
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()


def connect_db(app):    
    db.app = app
    db.init_app(app)



class User(db.Model):
    
    __tablename__ = "users"
    
    # @classmethod
    # def get_by_species(cls, species):
    #     return cls.query.filter_by(species=species).all()
    
    # @classmethod
    # def get_all_hungry(cls):
    #     return cls.query.filter(Pet.hunger > 20).all()
        
    
    def __repr__(self):
        u=self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} img_url={u.img_url}>"
    
    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    first_name = db.Column(db.String(50),
                     nullable=False)
    last_name = db.Column(db.String(100))
    img_url = db.Column(db.String(800),
                       nullable=False)
    
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
