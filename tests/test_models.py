import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine
from models.connect import conn,cursor
from database.setup import create_tables


create_tables()

class TestModels(unittest.TestCase):
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
        # Mocking database response
        self.cursor.fetchall.return_value = [(1, "John Doe"), (2, "John Doe")]
        authors = Author.get_all_authors(self.cursor)
        # Checking if execute method was called with correct argument
        self.cursor.execute.assert_called_once_with("SELECT * FROM authors")
        # Checking if authors were fetched correctly
        self.assertEqual(len(authors), 2)
        self.assertEqual(authors[0].id, 1)
        self.assertEqual(authors[0].name, "John Doe")
        self.assertEqual(authors[1].id, 2)
        self.assertEqual(authors[1].name, "John Doe")




    def test_saves_articles(self):
        # Clear the articles table
        cursor.execute("DELETE FROM articles")
        cursor.connection.commit()

        # Create and save an article
        article = Article(title="Test Title", content="Test Content", author_id=1, magazine_id=1)
        article.save()

        # Verify that the article was saved
        sql = "SELECT * FROM articles WHERE id = ?"
        row = cursor.execute(sql, (article.id,)).fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[1], "Test Title")
        self.assertEqual(row[2], "Test Content")
        self.assertEqual(row[3], 1)
        self.assertEqual(row[4], 1)

if __name__ == "__main__":
    unittest.main()