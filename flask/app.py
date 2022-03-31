from distutils.log import debug
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime  import date, datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/ggggg/Documents/gym/blogy/flask/blog.db'
db = SQLAlchemy(app)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(30))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)


@app.route('/')
def index():
    posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = BlogPost.query.filter_by(id=post_id).one()
    date_posted = post.date_posted.strftime("%d %b %Y")
    # date_posted = post.date_posted.strftime("%B the %d of %Y is %A at %I:%M %p")
    return render_template('post.html', post=post)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/addpost', methods=['GET', 'POST'])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']
    # return '<h2> Title: {} subtitle:{} author: {} content:{} </h2>'.format(title, subtitle, author, content)

    post = BlogPost(title=title, subtitle=subtitle, author=author, content=content, date_posted=datetime.now())
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)