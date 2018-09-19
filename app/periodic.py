from flask_script import Manager
import xml.etree.ElementTree as ET
import urllib.request
from app import app, db, models
from dateutil.parser import parse
import json


namespaces = {
'atom':"http://www.w3.org/2005/Atom"
}

def periodic():
    
    
    # Read in the blog json
    blogs = []
    with open('blogs.json', 'r') as blogs_json:
        blogs = json.parse(blogs_json.read())
    
    for blog in blogs['blogs']:
        
        # First, make sure the blog is in the db
        cur_blog = db.session.query(models.Blog).filter(feed_url = blog['feed_url'])
        if cur_blog is None:
            # New blog, add it!
            cur_blog = models.Blog()
        
        # Update all the attributes, in case any changed
        cur_blog.url = blog['url']
        cur_blog.name = blog.['name']
        
        url = "https://derekweitzel.com/feed.xml"
        req = urllib.request.Request(
            url, 
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
        updated = parse(tree.find('atom:updated', namespaces))
        if updated <= cur_blog.last_update:
            # We already have the most up to date blog entry
            continue
        
        for child in tree:
            print(child.tag, child.attrib)
        print(tree)
        
        
        
        
        print(tree.tag)
        print(tree.attrib)
        for entry in tree.findall('atom:entry', namespaces):
            print(entry)
            post = models.Post()
            #post.id = entry.find("./xmlns:id", namespaces).text
            #post.origin_blog = entry.find("")
            post.title = entry.find("atom:title", namespaces).text
            post.content = entry.find("atom:content", namespaces).text
            post.date = parse(entry.find("atom:updated", namespaces).text)
            post.post_url = entry.find("atom:link", namespaces).attrib['href']
            post.origin_blog = "Derek"
            print(post)
            db.session.add(post)

        db.session.commit()