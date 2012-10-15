from temp import db, Book, Author, User

print Book.query.all()
print User.query.filter_by(username='admin').first().password

