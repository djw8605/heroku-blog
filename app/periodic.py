from flask_script import Manager
import xml.etree.ElementTree as ET
import urllib.request
from app import app, db, models
from dateutil.parser import parse
import json
import sqlalchemy
import pytz

utc=pytz.UTC


namespaces = {
'atom':"http://www.w3.org/2005/Atom"
}

def periodic():
    
    
    # Read in the blog json
    blogs = []
    with open('blogs.json', 'r') as blogs_json:
        blogs = json.loads(blogs_json.read())
    
    for blog in blogs['blogs']:
        
        # First, make sure the blog is in the db
        cur_blog = db.session.query(models.Blog).filter(models.Blog.feed_url == blog['feed_url']).first()
        if not cur_blog:
            cur_blog = models.Blog()
            cur_blog.feed_url = blog['feed_url']
        
        # Update all the attributes, in case any changed
        cur_blog.url = blog['url']
        cur_blog.name = blog['name']

        req = urllib.request.Request(
            cur_blog.feed_url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
            )

        f = urllib.request.urlopen(req)
        atom_feed = f.read().decode('utf-8')
        #print(atom_feed)

        #feed = urllib.urlopen("https://derekweitzel.com/feed.xml")
        #atom_feed = feed.read()
        #print atom_feed
        tree = ET.fromstring(atom_feed)
        
        # Get the blog updated date, see if we have to do anything else
        updated = parse(tree.find('atom:updated', namespaces).text)
        
        if cur_blog.last_update and updated <= utc.localize(cur_blog.last_update):
            # We already have the most up to date blog entry
            print("No need to do anything, we've updated most recent")
            db.session.add(cur_blog)
            db.session.commit()
            continue
        
        cur_blog.last_update = updated
        
        
        print(tree.tag)
        print(tree.attrib)
        for entry in tree.findall('atom:entry', namespaces):
            post_id = entry.find("atom:id", namespaces).text
            post_date = parse(entry.find("atom:updated", namespaces).text)
            # Check if the post already exists
            post = db.session.query(models.Post).filter(models.Post.post_id == post_id).first()
            if not post:
                post = models.Post()
            if not post.date or post.date < post_date:
                # Update the post
                post.title = entry.find("atom:title", namespaces).text
                post.content = entry.find("atom:content", namespaces).text
                post.date = post_date
                post.post_url = entry.find("atom:link", namespaces).attrib['href']
                post.post_id = post_id
                cur_blog.posts.append(post)
                print("Discovered new post: {}".format(post.title))

        db.session.add(cur_blog)
        db.session.commit()