from database.setup import create_tables
from database.connection import get_db_connection
from models.article import Article
from models.author import Author
from models.magazine import Magazine

def main():
  
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
    author = Author(name=author_name, conn=conn, cursor=cursor)
    author.save()

    # Create a magazine
    magazine = Magazine(name=magazine_name, category=magazine_category, conn=conn, cursor=cursor)
    magazine.save()

    # Create an article
    article = Article(title=article_title, content=article_content, author_id=author.id, magazine_id=magazine.id, conn=conn, cursor=cursor)
    article.save()

    # Query the database for inserted records
    cursor.execute('SELECT * FROM magazines')
    magazines = cursor.fetchall()

    cursor.execute('SELECT * FROM authors')
    authors = cursor.fetchall()

    cursor.execute('SELECT * FROM articles')
    articles = cursor.fetchall()

    # Display results
    print("\nMagazines:")
    for mag in magazines:
        print(Magazine(mag[0], mag[1], mag[2]))

    print("\nAuthors:")
    for auth in authors:
        print(Author(auth[0], auth[1]))

    print("\nArticles:")
    for art in articles:
        print(Article(art[0], art[1], art[2], art[3], art[4]))

    # Example usage of the Article class
    new_article = Article(title='My First Article', content='This is the content of my first article.', author_id=author.id, magazine_id=magazine.id, conn=conn, cursor=cursor)
    new_article.save()
    print(f'New article created with ID: {new_article.id}')

   
    conn.close()

if __name__ == "__main__":
    main()
