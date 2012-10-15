#from flask import Flask, render_template
from flask import *
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form, TextField, Required
from md5 import md5


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = "T\xd6\\p\xf9\x8e\xd6\xc0TL\xdf\x92\x080Q\xbf\xf0)\xd1&'\xeb\xb0\x05"
db = SQLAlchemy(app)

library = db.Table('library',
    db.Column('author_id', db.Integer, db.ForeignKey('author.id')),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id')))

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return '<Author %r>' % self.name

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    authors = db.relationship('Author', secondary=library,
        backref=db.backref('books', lazy='dynamic'))
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return '<Book %r>' % self.name


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(32))

    def __init__(self, username, password):
        self.username = username
        self.password = md5(password).hexdigest()

    def __repr__(self):
        return '<User %r>' % self.username

#@app.route('/images/<filename>')
#def images(filename=None):
#    if filename:
#        return url_for('static', filename='images/'+filename)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == md5(request.form['password']).hexdigest():
            print request.form['username']
            session['username'] = request.form['username']
    print '!!!'
    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('hello.html')


if __name__ == '__main__':
    app.run()