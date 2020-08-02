
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
        Post.query.delete()
    
    def tearDown(self):
        """Clean up any additions/changes made in the db."""
        
        db.session.rollback()
        
    def test_full_name(self):
        """Tests if calling full_name method works."""
        
        user = User(first_name='Frank', last_name='Ocean', img_url='https://a.espncdn.com/photo/2015/1212/r35307_1296x729_16-9.jpg')

        db.session.add(user)
        db.session.commit()
        
        singer = user.full_name
        self.assertEqual('FrankOcean', singer)
    

 