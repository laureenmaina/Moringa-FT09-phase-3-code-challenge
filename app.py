from database.setup import create_tables
from database.connection import get_db_connection
from models.article import Article
from models.author import Author
from models.magazine import Magazine

def main():
    # Initialize the database and create tables
    create_tables()

    # Collect user input
    author_name = input("Enter author's name: ")
    magazine_name = input("Enter magazine name: ")
    magazine_category = input("Enter magazine category: ")
    article_title = input("Enter article title: ")
    article_content = input("Enter article content: ")

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create an author
    cursor.execute('INSERT INTO authors (name) VALUES (?)', (author_name,))
    author_id = cursor.lastrowid

    # Create a magazine
    cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (magazine_name, magazine_category))
    magazine_id = cursor.lastrowid

    # Create an article
    cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)',
                   (article_title, article_content, author_id, magazine_id))
    conn.commit()

    # Query the database for inserted records
    cursor.execute('SELECT * FROM magazines')
    magazines = cursor.fetchall()

    cursor.execute('SELECT * FROM authors')
    authors = cursor.fetchall()

    cursor.execute('SELECT * FROM articles')
    articles = cursor.fetchall()

    conn.close()

    # Display results
    print("\nMagazines:")
    for magazine in magazines:
        print(Magazine(magazine[0], magazine[1], magazine[2]))

    print("\nAuthors:")
    for author in authors:
        print(Author(author[0], author[1]))

    print("\nArticles:")
    for article in articles:
        print(Article(article[0], article[1], article[2], article[3], article[4]))

    # Example usage of the Article class
    new_article = Article(title='My First Article', content='This is the content of my first article.', author_id=author_id, magazine_id=magazine_id)
    new_article.save()
    print(f'New article created with ID: {new_article.id}')

    # Fetch and print all articles
    all_articles = Article.get_all()
    print('All Articles:')
    for article in all_articles:
        print(article)

    # Fetch an article by ID
    article_id = new_article.id
    fetched_article = None
    for article in all_articles:
        if article.id == article_id:
            fetched_article = article
            break

    if fetched_article:
        print(f'Fetched Article: {fetched_article}')
        print(f'Author: {fetched_article.author}')
        print(f'Magazine: {fetched_article.magazine}')

    # Update an existing article
    fetched_article.title = 'Updated Article Title'
    fetched_article.content = 'Updated content of the article.'
    fetched_article.save()
    print(f'Updated Article: {fetched_article}')

    # Fetch and print all articles again to see the update
    all_articles = Article.get_all()
    print('All Articles After Update:')
    for article in all_articles:
        print(article)

if __name__ == "__main__":
    main()
