

#from app import app, db
from app import db
from sqlalchemy.orm import relationship
import datetime

class Post(db.Model):
    """
    Table schema
    """
    __tablename__ = "posts"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Text(), nullable=False)
    origin_blog = db.Column(db.Integer, db.ForeignKey('blogs.id'))
    date = db.Column(db.DateTime(), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    title = db.Column(db.Text())
    post_url = db.Column(db.Text())
    
    blog = relationship("Blog", back_populates="posts")
    
    
    def __repr__(self):
        return "Post: {}.".format(self.title)
    
    @staticmethod
    def get_posts():
        return Post.query.order_by(Post.date.desc()).limit(10).all()
    

class Blog(db.Model):
    """
    Blog model
    """
    __tablename__ = "blogs"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.Text())
    feed_url = db.Column(db.Text())
    last_update = db.Column(db.DateTime())
    name = db.Column(db.Text())
    posts = relationship("Post", order_by=Post.id, back_populates="blog")
    
    

