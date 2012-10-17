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

class AddForm(Form):
    new = TextField('new_value', validators=[Required(), Length(min=2, max=30, message='Invalid length (allowed 2-20 symbols)')])

class BookAuthorForm(Form):
    author_id = HiddenField('author_id', validators=[Required()])
    book_id = HiddenField('book_id', validators=[Required()])


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
    admin = db.Column(db.Boolean)

    def __init__(self, username, password, ifadmin = False):
        self.username = username
        self.password = md5(password).hexdigest()
        self.admin = ifadmin

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if request.method == 'POST' and login_form.validate():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user and user.password == md5(login_form.password.data).hexdigest():
            session['username'] = login_form.username.data
    return redirect(url_for('index'))

def user(_session):
    if 'username' in session: return User.query.filter_by(username = session['username']).first()
    else: return None

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/')
def index():
    login_form = LoginForm()
    return render_template('main.html', user = user(session), form=login_form)

@app.route('/del-author', methods=['GET', 'POST'])
def del_author():
    del_form = DelForm()
    if request.method == 'POST' and del_form.validate():
        db.session.delete(Author.query.get(del_form.num.data))
        db.session.commit()
        return 'True'
    else:
        return 'False'

@app.route('/edit-author', methods=['GET', 'POST'])
def edit_author():
    edit_form = EditForm()
    if request.method == 'POST' and edit_form.validate():
        Author.query.filter_by(id = edit_form.num.data).first().name = edit_form.new_value.data
        db.session.commit()
        return Author.query.filter_by(id = edit_form.num.data).first().name
    else:
        return 'False'

@app.route('/del-book', methods=['GET', 'POST'])
def del_book():
    del_form = DelForm()
    if request.method == 'POST' and del_form.validate():
        db.session.delete(Book.query.get(del_form.num.data))
        db.session.commit()
        return 'True'
    else:
        return 'False'

@app.route('/edit-book', methods=['GET', 'POST'])
def edit_book():
    edit_form = EditForm()
    if request.method == 'POST' and edit_form.validate():
        Book.query.filter_by(id = edit_form.num.data).first().name = edit_form.new_value.data
        db.session.commit()
        return Book.query.filter_by(id = edit_form.num.data).first().name
    else:
        return 'False'
@app.route('/del-book-author', methods=['GET', 'POST'])
def del_book_author():
    form = BookAuthorForm()
    if request.method == 'POST' and form.validate():
        book = Book.query.get(form.book_id.data)
        author = Author.query.get(form.author_id.data)
        if author in book.authors:
            del book.authors[book.authors.index(author)]
        db.session.commit()
        return render_template('book_authors.html', user = user(session), book = Book.query.get(form.book_id.data))
    else:
        return 'False'

@app.route('/add-book', methods=['GET', 'POST'])
def add_book():
    form = AddForm()
    if request.method == 'POST' and form.validate():
        new_book = Book(form.new.data)
        db.session.add(new_book)
        db.session.commit()
        return 'True'
    else:
        return 'False'

@app.route('/add-author', methods=['GET', 'POST'])
def add_author():
    form = AddForm()
    if request.method == 'POST' and form.validate():
        new_author = Author(form.new.data)
        db.session.add(new_author)
        db.session.commit()
        return 'True'
    else:
        return 'False'

@app.route('/add-book-author', methods=['GET', 'POST'])
def add_book_author():
    form = BookAuthorForm()
    if request.method == 'POST' and form.validate():
        book = Book.query.get(form.book_id.data)
        add_author = Author.query.get(form.author_id.data)
        book.authors.append(add_author)
        db.session.commit()
        return render_template('book_authors.html', user = user(session), book = Book.query.get(form.book_id.data))
    else:
        return 'False'


@app.route('/book-filter')
def book_filter():
    del_form = DelForm()
    b_filter = request.args.get('bfilter', '')
    books = [book for book in Book.query.order_by(Book.id.desc()).all() if b_filter.lower() in book.name.lower()+str(book.authors).lower()]
    return render_template('books_list.html', books = books, user = user(session), del_form=del_form)

@app.route('/author-filter')
def author_filter():
    del_form = DelForm()
    edit_form = EditForm()
    a_filter = request.args.get('afilter', '')
    authors = [author for author in Author.query.order_by(Author.id.desc()).all() if a_filter.lower() in author.name.lower()]
    return render_template('authors_list.html', authors = authors, user = user(session), del_form=del_form, edit_form=edit_form)

if __name__ == '__main__':
    app.run()