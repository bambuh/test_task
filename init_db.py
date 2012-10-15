from temp import db, Book, Author, User
db.create_all()

book1 = Book('ABC')
book2 = Book('DEF')
book3 = Book('GHI')
book4 = Book('FRG dfgdf')
book5 = Book('Qdfg fgff')
author1 = Author('Sam')
author2 = Author('Peter')
author3 = Author('Amanda')
author4 = Author('Robert')
author5 = Author('Loise')
book1.authors = [author1, author2]
author3.books = [book5, book1]

db.session.add(book1)
db.session.add(book2)
db.session.add(book3)
db.session.add(book4)
db.session.add(book5)
db.session.add(author1)
db.session.add(author2)
db.session.add(author3)
db.session.add(author4)
db.session.add(author5)
db.session.commit()
print book1.authors

admin = User('admin', 'admin')
guest = User('guest', 'guest')
db.session.add(admin)
db.session.add(guest)
db.session.commit()