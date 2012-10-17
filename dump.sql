BEGIN TRANSACTION;
CREATE TABLE user (
	id INTEGER NOT NULL, 
	username VARCHAR(80), 
	password VARCHAR(32), 
	admin BOOLEAN, 
	PRIMARY KEY (id), 
	UNIQUE (username), 
	CHECK (admin IN (0, 1))
);
INSERT INTO "user" VALUES(1,'admin','21232f297a57a5a743894a0e4a801fc3',1);
INSERT INTO "user" VALUES(2,'guest','084e0343a0486ff05530df6c705c8bb4',0);
INSERT INTO "user" VALUES(3,'vasya','151b1c02484da0567d77ef508602e885',1);
CREATE TABLE author (
	id INTEGER NOT NULL, 
	name VARCHAR(30), 
	PRIMARY KEY (id)
);
INSERT INTO "author" VALUES(1,'R. Helm');
INSERT INTO "author" VALUES(2,'J. Vlissides');
INSERT INTO "author" VALUES(3,'R. Johnson');
INSERT INTO "author" VALUES(4,'E. Gamma');
INSERT INTO "author" VALUES(5,'Б. Акунин');
INSERT INTO "author" VALUES(6,'Масару Ибука');
INSERT INTO "author" VALUES(7,'Р. Киосаки');
INSERT INTO "author" VALUES(8,'Ш. Лектер');
INSERT INTO "author" VALUES(9,'Д. Трамп');
INSERT INTO "author" VALUES(10,'Мураками');
INSERT INTO "author" VALUES(11,'Достоевский');
INSERT INTO "author" VALUES(12,'Д. Анкона');
INSERT INTO "author" VALUES(13,'Х. Бресман');
CREATE TABLE book (
	id INTEGER NOT NULL, 
	name VARCHAR(50), 
	PRIMARY KEY (id)
);
INSERT INTO "book" VALUES(1,'Design Patterns');
INSERT INTO "book" VALUES(2,'Азазель');
INSERT INTO "book" VALUES(3,'Алмазная Колесница');
INSERT INTO "book" VALUES(4,'Квест');
INSERT INTO "book" VALUES(5,'После трёх уже поздно');
INSERT INTO "book" VALUES(6,'Богатый папа, бедный папа');
INSERT INTO "book" VALUES(7,'Why We Want You to Be Rich');
INSERT INTO "book" VALUES(8,'Курочка Ряба');
INSERT INTO "book" VALUES(9,'Команды прорыва. Источники инноваций и лидерства в отрасли');
CREATE TABLE library (
	author_id INTEGER, 
	book_id INTEGER, 
	FOREIGN KEY(author_id) REFERENCES author (id), 
	FOREIGN KEY(book_id) REFERENCES book (id)
);
INSERT INTO "library" VALUES(1,1);
INSERT INTO "library" VALUES(4,1);
INSERT INTO "library" VALUES(2,1);
INSERT INTO "library" VALUES(3,1);
INSERT INTO "library" VALUES(5,2);
INSERT INTO "library" VALUES(5,3);
INSERT INTO "library" VALUES(5,4);
INSERT INTO "library" VALUES(6,5);
INSERT INTO "library" VALUES(7,6);
INSERT INTO "library" VALUES(8,6);
INSERT INTO "library" VALUES(7,7);
INSERT INTO "library" VALUES(9,7);
INSERT INTO "library" VALUES(8,7);
INSERT INTO "library" VALUES(13,9);
INSERT INTO "library" VALUES(12,9);
COMMIT;
