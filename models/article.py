from models.conn import CURSOR,CONN

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

       
    def __repr__(self):
        return f'<Article {self.title}>'
    

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            TypeError("Id must be of type int")
        self._id = value


    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not (5 <= len(value) <= 50):
             ValueError("Title must be of type str and must be between 5 and 50 characters inclusive")
        self._title = value

    @property
    def author(self):
        from models.author import Author
        sql = """
            SELECT authors.id, authors.name
            FROM authors
            INNER JOIN articles 
            ON authors.id = articles.author_id
            WHERE articles.id = ?
        """
        CURSOR.execute(sql, (self.id,))
        row = CURSOR.fetchone()
        if row:
            return Author(row[0], row[1])
        else:
            return None

    @property
    def magazine(self):
        from models.magazine import Magazine
        sql = """
            SELECT magazines.id, magazines.name, magazines.category
            FROM magazines
            INNER JOIN articles
            ON magazines.id = articles.magazine_id
            WHERE articles.id = ?
        """
        CURSOR.execute(sql, (self.id,))
        row = CURSOR.fetchone()
        if row:
            return Magazine(row[0], row[1], row[2])
        else:
            return None
        
    def save(self):
       
        sql = """
                INSERT INTO articles (author_id,magazine_id,title,content,)
                VALUES (?, ?, ?,?)
        """

        CURSOR.execute(sql, (self.title,self.content,self.author_id,self.magazine_id))
        CONN.commit()

        self.id = CURSOR.lastrowid
      
        

    @classmethod
    def get_all(cls):
        """Return a list containing one Employee object per table row"""
        sql = """
            SELECT *
            FROM articles
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]

