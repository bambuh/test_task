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
        return '%r' % self.name

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
    admin = db.Column(db.Boolean)

    def __init__(self, username, password, admin = False):
        self.username = username
        self.password = md5(password).hexdigest()
        self.admin = admin

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

def user(_session):
    if 'username' in session: return session['username']
    else: return None

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/')
def index():
    # if 'username' in session: user = session['username']
    # else: user = None
    return render_template('hello2.html', user = user(session))

@app.route('/book-filter')
def book_filter():
    b_filter = request.args.get('bfilter', '')
    books = [book for book in Book.query.all() if b_filter.lower() in book.name.lower()+str(book.authors).lower()]
    print 'BOOOOKS',b_filter.lower(),book.name.lower()+str(book.authors).lower(), books
    return render_template('books_list.html', books = books, user = user(session))
    # return redirect(url_for('index'))

@app.route('/author-filter')
def author_filter():
    a_filter = request.args.get('afilter', '')
    authors = [author for author in Author.query.all() if a_filter.lower() in author.name.lower()]
    print "aaaa", authors
    return render_template('authors_list.html', authors = authors, user = user(session))
    # return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()