from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:cheese@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


# I created the class Blog that allows blog posts to be made...
class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(255))

    def __init__(self, title, body):
        self.title = title
        self.body = body

# home route...
@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        blogs = Blog.query.all()

    return render_template('mainpage.html', blogs = blogs )


# make a viewpost access point....
@app.route('/viewpost', methods =['GET'])
def viewpost():
    blog_id = request.args.get('id')
    blog = Blog.query.get(blog_id)
    return render_template('viewpost.html', blog = blog)

# make a newpost access point....
@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
        
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        blog_post = Blog(title, body)
        db.session.add(blog_post)
        db.session.commit()
        return render_template('viewpost.html', blog = blog_post)

    return render_template('newpost.html')



if __name__ == '__main__':
    app.run()