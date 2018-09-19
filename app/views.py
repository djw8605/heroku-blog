from app import models
from app import app
from app import db

from flask import render_template




@app.route('/')
def index():
    posts = models.Post.get_posts()
    blogs = db.session.query(models.Blog).all()
    
    return render_template('index.tmpl', posts=posts, blogs = blogs)

        
        
    
    
    

    
    
    
