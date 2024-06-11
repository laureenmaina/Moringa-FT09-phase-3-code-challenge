import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine
from models.connect import conn,cursor
from database.setup import create_tables


create_tables()

class TestModels(unittest.TestCase):

    def setUp(self):
        # Ensure database is clean before each test
        cursor.execute("DELETE FROM articles")
        cursor.execute("DELETE FROM authors")
        cursor.execute("DELETE FROM magazines")
        conn.commit()

    def test_author_creation(self):
        author = Author(1, "John Doe")
        self.assertEqual(author.name, "John Doe")

    def test_article_creation(self):
        article = Article(1, "Test Title", "Test Content", 1, 1)
        self.assertEqual(article.title, "Test Title")

    def test_magazine_creation(self):
        magazine = Magazine(1, "Tech Weekly")
        self.assertEqual(magazine.name, "Tech Weekly")

    def test_get_all_authors(self):
        author1 = Author(name="John Doe")
        author1.save()

        author2 = Author(name="Jane Doe")
        author2.save()

        authors = Author.get_all_authors()

        self.assertEqual(len(authors), 2)

        self.assertEqual(authors[0].name, "John Doe")
        self.assertEqual(authors[1].name, "Jane Doe")

    def test_saves_articles(self):
        cursor.execute("DELETE FROM articles")
        cursor.connection.commit()

        article = Article(title="Test Title", content="Test Content", author_id=1, magazine_id=1)
        article.save()

        sql = "SELECT * FROM articles WHERE id = ?"
        row = cursor.execute(sql, (article.id,)).fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[1], "Test Title")
        self.assertEqual(row[2], "Test Content")
        self.assertEqual(row[3], 1)
        self.assertEqual(row[4], 1)

    def test_invalid_author_creation(self):
        with self.assertRaises(ValueError):
            author = Author(name="")
            author.save()

        with self.assertRaises(ValueError):
            author = Author(name=123)
            author.save()

    def test_author_magazines(self):
        author = Author(name="John Doe")
        author.save()

        # Create magazines
        cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", ("Magazine 1", "Tech"))
        magazine_id = cursor.lastrowid
        cursor.execute("INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
                       ("Article 1", "Content 1", author.id, magazine_id))
        cursor.execute("INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
                       ("Article 2", "Content 2", author.id, magazine_id))
        conn.commit()

        magazines = author.magazines()

    def test_author_update(self):
        author = Author(name="John Doe")
        author.save()

       
        author.name = "Jane Doe"
        author.save()

       
        sql = "SELECT * FROM authors WHERE id = ?"
        row = cursor.execute(sql, (author.id,)).fetchone()
        self.assertEqual(row[1], "Jane Doe")

    

if __name__ == "__main__":
    unittest.main()