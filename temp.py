#from flask import Flask, render_template
from flask import *
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form, TextField, Required, PasswordField, DecimalField, HiddenField, Length
from md5 import md5


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = "T\xd6\\p\xf9\x8e\xd6\xc0TL\xdf\x92\x080Q\xbf\xf0)\xd1&'\xeb\xb0\x05"
db = SQLAlchemy(app)

library = db.Table('library',
    db.Column('author_id', db.Integer, db.ForeignKey('author.id')),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id')))

class LoginForm(Form):
    username = TextField('Login', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])

class DelForm(Form):
    num = HiddenField('id', validators=[Required()])

class EditForm(Form):
    num = HiddenField('id', validators=[Required()])
    new_value = TextField('new_value', validators=[Required(), Length(min=2, max=30, message='Invalid length (allowed 2-20 symbols)')])

class BookAuthorForm(Form):
    author_id = HiddenField('author_id', validators=[Required()])
    book_id = HiddenField('book_id', validators=[Required()])


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
    login_form = LoginForm()
    # if request.method == 'POST':
    #     user = User.query.filter_by(username=request.form['username']).first()
    #     if user and user.password == md5(request.form['password']).hexdigest():
    #         print request.form['username']
    #         session['username'] = request.form['username']
    if request.method == 'POST' and login_form.validate():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user and user.password == md5(login_form.password.data).hexdigest():
            print login_form.username.data
            session['username'] = login_form.username.data
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
    login_form = LoginForm()
    print login_form, login_form.username
    return render_template('hello2.html', user = user(session), form=login_form)

@app.route('/del-author', methods=['GET', 'POST'])
def del_author():
    del_form = DelForm()
    if request.method == 'POST' and del_form.validate():
        print del_form.num.data
        print Author.query.filter_by(id = del_form.num.data).first()
        db.session.delete(Author.query.filter_by(id = del_form.num.data).first())
        print '111'
        db.session.commit()
        return 'True'
    else:
        return 'False'

@app.route('/edit-author', methods=['GET', 'POST'])
def edit_author():
    edit_form = EditForm()
    if request.method == 'POST' and edit_form.validate():
        Author.query.filter_by(id = edit_form.num.data).first().name = edit_form.new_value.data
        print '111'
        db.session.commit()
        return Author.query.filter_by(id = edit_form.num.data).first().name
    else:
        return 'False'

@app.route('/del-book', methods=['GET', 'POST'])
def del_book():
    del_form = DelForm()
    print del_form
    if request.method == 'POST' and del_form.validate():
        print del_form.num.data
        print Book.query.filter_by(id = del_form.num.data).first()
        db.session.delete(Book.query.filter_by(id = del_form.num.data).first())
        print '111'
        db.session.commit()
        return 'True'
    else:
        return 'False'

@app.route('/edit-book', methods=['GET', 'POST'])
def edit_book():
    edit_form = EditForm()
    if request.method == 'POST' and edit_form.validate():
        Book.query.filter_by(id = edit_form.num.data).first().name = edit_form.new_value.data
        print '111'
        db.session.commit()
        return Book.query.filter_by(id = edit_form.num.data).first().name
    else:
        return 'False'

@app.route('/add_book_author', methods=['GET', 'POST'])
def add_book_author():
    form = BookAuthorForm()
    if request.method == 'POST' and form.validate():
        Book.query.filter_by(id = form.book_id.data).first().authors.append(Author.query.filter_by(id = form.author_id.data).first())
        print '111'
        db.session.commit()
        return render_template('book_authors.html', user = user(session), authors = Book.query.filter_by(id = form.book_id.data).first().authors)
    else:
        return 'False'


@app.route('/book-filter')
def book_filter():
    del_form = DelForm()
    b_filter = request.args.get('bfilter', '')
    books = [book for book in Book.query.all() if b_filter.lower() in book.name.lower()+str(book.authors).lower()]
    print 'BOOOOKS',b_filter.lower(),book.name.lower()+str(book.authors).lower(), books
    return render_template('books_list.html', books = books, user = user(session), del_form=del_form)
    # return redirect(url_for('index'))

@app.route('/author-filter')
def author_filter():
    del_form = DelForm()
    edit_form = EditForm()
    a_filter = request.args.get('afilter', '')
    authors = [author for author in Author.query.all() if a_filter.lower() in author.name.lower()]
    print "aaaa", authors
    return render_template('authors_list.html', authors = authors, user = user(session), del_form=del_form, edit_form=edit_form)
    # return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()