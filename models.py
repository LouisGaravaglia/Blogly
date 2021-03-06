
from flask_sqlalchemy import SQLAlchemy
import datetime



db = SQLAlchemy()


def connect_db(app):    
    db.app = app
    db.init_app(app)

# ===========================================================   "users"   =========================================================== 

class User(db.Model):
    
    __tablename__ = "users"
    

    def __repr__(self):
        u=self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} img_url={u.img_url}>"
    
    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    first_name = db.Column(db.String(50),
                     nullable=False)
    last_name = db.Column(db.String(100))
    img_url = db.Column(db.String(100),
                       nullable=False)
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")
    
    
    @property
    def full_name(self):
        """Return full name of user."""
        
        return f"{self.first_name}{self.last_name}"        
    
# ===========================================================   "posts"   =========================================================== 

class Post(db.Model):
    
    __tablename__ = "posts"
        
    
    def __repr__(self):
        p=self
        return f"<User id={p.id} title={p.title} content={p.content} created_at={p.created_at} owner_id={p.owner_id}>"
    
    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    title = db.Column(db.String(50),
                     nullable=False)
    content = db.Column(db.String(1000),
                     nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    

    
    @property
    def friendly_date(self):
        """Return nicely-formatted date."""
        
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")
        
# ===========================================================   "posts_tags"   =========================================================== 
    
class PostTag(db.Model):
    """Tag on a post."""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

# ===========================================================   "tags"   =========================================================== 

class Tag(db.Model):
    """Tag that can be added to posts."""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship(
        'Post',
        secondary="posts_tags",
        backref="tags",
    )


    
      
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
