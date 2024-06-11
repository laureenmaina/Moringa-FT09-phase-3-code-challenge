from models.connect import cursor, conn
   
class Article:
    
    def __init__(self, id=None, title=None, content=None, author_id=None, magazine_id=None):
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
        if not isinstance(value, int) and value is not None:
            raise TypeError("Id must be of type int")
        self._id = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not (5 <= len(value) <= 50):
            raise ValueError("Title must be of type str and must be between 5 and 50 characters inclusive")
        self._title = value

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if not isinstance(value, str):
            raise ValueError("Content must be of type str")
        self._content = value

    @property
    def author_id(self):
        return self._author_id

    @author_id.setter
    def author_id(self, value):
        if not isinstance(value, int):
            raise ValueError("Author ID must be of type int")
        self._author_id = value

    @property
    def magazine_id(self):
        return self._magazine_id

    @magazine_id.setter
    def magazine_id(self, value):
        if not isinstance(value, int):
            raise ValueError("Magazine ID must be of type int")
        self._magazine_id = value

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
        cursor.execute(sql, (self.id,))
        row = cursor.fetchone()
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
        cursor.execute(sql, (self.id,))
        row = cursor.fetchone()
        if row:
            return Magazine(row[0], row[1], row[2])
        else:
            return None

    def save(self):
        if self.id is None:
            sql = """
                INSERT INTO articles (title, content, author_id, magazine_id)
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(sql, (self.title, self.content, self.author_id, self.magazine_id))
            conn.commit()
            self.id = cursor.lastrowid
        else:
            sql = """
                UPDATE articles
                SET title = ?, content = ?, author_id = ?, magazine_id = ?
                WHERE id = ?
            """
            cursor.execute(sql, (self.title, self.content, self.author_id, self.magazine_id, self.id))
            conn.commit()

    @classmethod
    def instance_from_db(cls, row):
        return cls(row[0], row[1],row[2],row[3],row[4])

    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM articles
        """
        rows = cursor.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS articles
        """
        cursor.execute(sql)
        conn.commit()
    