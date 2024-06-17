import unittest
import sqlite3
from models.author import Author
from models.article import Article
from models.magazine import Magazine

def create_tables():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE magazines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author_id INTEGER,
            magazine_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors(id),
            FOREIGN KEY (magazine_id) REFERENCES magazines(id)
        )
    """)
    conn.commit()
    return conn, cursor

class TestModels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn, cls.cursor = create_tables()

    def setUp(self):
        self.conn = TestModels.conn
        self.cursor = TestModels.cursor

    def test_author_creation(self):
        author = Author(name="John Doe", conn=self.conn, cursor=self.cursor)
        self.assertEqual(author.name, "John Doe")

    def test_article_creation(self):
        article = Article(title="Test Title", content="Test Content", author_id=1, magazine_id=1, conn=self.conn, cursor=self.cursor)
        self.assertEqual(article.title, "Test Title")

    def test_magazine_creation(self):
        magazine = Magazine(name="Tech Weekly", category="Tech", conn=self.conn, cursor=self.cursor)
        self.assertEqual(magazine.name, "Tech Weekly")

    def test_get_all_authors(self):
        self.cursor.execute("DELETE FROM authors")
        self.conn.commit()

        author1 = Author(name="John Doe", conn=self.conn, cursor=self.cursor)
        author1.save()

        author2 = Author(name="Jane Doe", conn=self.conn, cursor=self.cursor)
        author2.save()

        authors = Author.get_all_authors(self.conn, self.cursor)

        self.assertEqual(len(authors), 2)
        self.assertEqual(authors[0].name, "John Doe")
        self.assertEqual(authors[1].name, "Jane Doe")

    def test_saves_articles(self):
        self.cursor.execute("DELETE FROM articles")
        self.conn.commit()

        article = Article(title="Test Title", content="Test Content", author_id=1, magazine_id=1, conn=self.conn, cursor=self.cursor)
        article.save()

        sql = "SELECT * FROM articles WHERE id = ?"
        row = self.cursor.execute(sql, (article.id,)).fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[1], "Test Title")
        self.assertEqual(row[2], "Test Content")
        self.assertEqual(row[3], 1)
        self.assertEqual(row[4], 1)

    def test_invalid_author_creation(self):
        with self.assertRaises(ValueError):
            author = Author(name="", conn=self.conn, cursor=self.cursor)
            author.save()

        with self.assertRaises(ValueError):
            author = Author(name=123, conn=self.conn, cursor=self.cursor)
            author.save()

    def test_author_magazines(self):
        author = Author(name="John Doe", conn=self.conn, cursor=self.cursor)
        author.save()

        self.cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", ("Magazine 1", "Tech"))
        magazine_id = self.cursor.lastrowid
        self.cursor.execute("INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
                            ("Article 1", "Content 1", author.id, magazine_id))
        self.cursor.execute("INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
                            ("Article 2", "Content 2", author.id, magazine_id))
        self.conn.commit()

        magazines = author.magazines()
        self.assertEqual(len(magazines), 1)
        self.assertEqual(magazines[0].name, "Magazine 1")
        self.assertEqual(magazines[0].category, "Tech")

    def test_author_update(self):
        author = Author(name="John Doe", conn=self.conn, cursor=self.cursor)
        author.save()

        author.name = "Jane Doe"
        author.save()

        sql = "SELECT * FROM authors WHERE id = ?"
        row = self.cursor.execute(sql, (author.id,)).fetchone()
        self.assertEqual(row[1], "Jane Doe")

if __name__ == "__main__":
    unittest.main()
