
from unittest import TestCase
from app import app
from models import db, User, Post, Tag, PostTag


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False


app.config["TESTING"] = True
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Users."""
    
    def setUp(self):
        """Clean up any existing Users in the db."""
        Post.query.delete()
        User.query.delete()
        
        
        user = User(first_name='Frank', last_name='Ocean', img_url='https://a.espncdn.com/photo/2015/1212/r35307_1296x729_16-9.jpg')
        # tag = Tag(name='Acting')
        db.session.add(user)
        # db.session.add(tag)
        db.session.commit()
        
        post = Post(title='My home in como.', content='Its pretty dope.', user=user)

        db.session.add(post)
        db.session.commit()
        
        self.user_id = 6
        self.post_id = 5
        self.client = app.test_client()
    
    def tearDown(self):
        """Clean up any additions/changes made in the db."""
  
        db.session.rollback()
        
        
    def test_home_page(self):
        """ Making sure that the home page renders a list of posts. """

        with self.client as client:
            res = self.client.get("/")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(f'<a href="/posts/{self.post_id}">My home in como.</a>', html) 
            
    def test_user_page(self):
        """ Making sure that the user page renders correct html. """

        with self.client as client:
            res = self.client.get(f"/{self.user_id}")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<p class="user_name">Frank Ocean</p>', html) 
             
            
    
    def test_add_user(self):
        """ Making sure that we can add a user."""

        with self.client as client:
            d = {"first_name": "Barbara", "last_name": "Walters", "img_url": "https://r.ddmcdn.com/w_606/s_f/o_1.jpg"}
            res = self.client.post("/create_user", data=d, follow_redirects=True )
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Barbara Walters', html)   
            
            
    def test_users_page(self):
        """ Making sure that the user's post page renders correctly with post and tags. """

        with self.client as client:
            res = self.client.get(f"/users")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(f'<li class="users_item"><a href="/{self.user_id}">Frank Ocean</a></li>', html)
            
            
    def test_post_page(self):
        """ Making sure that the user's post page renders correctly with post and tags. """

        with self.client as client:
            res = self.client.get("/posts/{self.post_id}")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            # self.assertIn('<li class="users_item"><a href="/5">Frank Ocean</a></li>', html)              