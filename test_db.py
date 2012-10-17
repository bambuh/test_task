from temp import db, Book, Author, User

print Book.query.all()
print User.query.filter_by(username='admin').first().password
a = Book.query.get(1)
print a, a.authors
b = Author.query.filter_by(name='Aman').first()
print b
a.authors.append(b)
db.session.commit()
print a, a.authors

