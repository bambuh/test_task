from flask.ext.wtf import Form, TextField, Required, PasswordField, HiddenField, Length

class LoginForm(Form):
    username = TextField('Login', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])

class DelForm(Form):
    num = HiddenField('id', validators=[Required()])

class AuthorForm(Form):
    num = HiddenField('id', validators=[Required()])
    new_value = TextField('new_value', validators=[Required(), Length(min=2, max=20, message='Invalid length (allowed 2-20 symbols)')])

class BookForm(Form):
    num = HiddenField('id', validators=[Required()])
    new_value = TextField('new_value', validators=[Required(), Length(min=2, max=150, message='Invalid length (allowed 2-150 symbols)')])

class AddBookForm(Form):
    new = TextField('new_value', validators=[Required(), Length(min=2, max=150, message='Invalid length (allowed 2-150 symbols)')])

class AddAuthorForm(Form):
    new = TextField('new_value', validators=[Required(), Length(min=2, max=20, message='Invalid length (allowed 2-150 symbols)')])

class BookAuthorForm(Form):
    author_id = HiddenField('author_id', validators=[Required()])
    book_id = HiddenField('book_id', validators=[Required()])

