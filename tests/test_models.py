import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine

class TestModels(unittest.TestCase):
    def test_author_creation(self):
        author = Author(1, "John Doe")
        self.assertEqual(author.name, "John Doe")

    def test_article_creation(self):
        article = Article(1, "Test Title", "Test Content", 1, 1)
        self.assertEqual(article.title, "Test Title")

    def test_magazine_creation(self):
        magazine = Magazine(1, "Tech Weekly", "Technology")
        self.assertEqual(magazine.name, "Tech Weekly")
        self.assertEqual(magazine.category, "Technology")

if __name__ == "__main__":
    unittest.main()
    
author1 = Author("John Doe")
magazine1 = Magazine("The Daily News", "News")
article1 = Article(author1, magazine1, "New Developments in AI")

# Test methods
print(author1.articles())
print(magazine1.articles())
print(magazine1.contributors())
print(magazine1.article_titles())
print(magazine1.contributing_authors())
