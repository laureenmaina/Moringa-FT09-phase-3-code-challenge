from models.connect import conn, cursor as default_cursor,cursor

class Author:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    def __repr__(self):
        return f'<Author {self.name}>'

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            TypeError("Id must be of type int")
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value) <= 0:
            raise ValueError("Name must be a non-empty string")
        self._name = value

    def articles(self, cursor=default_cursor):
        from models.article import Article
        sql = """
            SELECT articles.id, articles.title, articles.content, articles.author_id, articles.magazine_id
            FROM articles
            INNER JOIN authors ON authors.id = articles.author_id
            WHERE authors.id = ?
        """
        cursor.execute(sql, (self.id,))
        rows = cursor.fetchall()
        return [Article(row[0], row[1], row[2], row[3], row[4]) for row in rows]

    def magazines(self, cursor=default_cursor):
        from models.magazine import Magazine
        sql = """
            SELECT DISTINCT magazines.id, magazines.name, magazines.category
            FROM magazines
            INNER JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        """
        cursor.execute(sql, (self.id,))
        rows = cursor.fetchall()
        return [Magazine(row[0], row[1], row[2]) for row in rows]

    def save(self, cursor=default_cursor):
        if self.id is None:
            sql = """
                INSERT INTO authors (name)
                VALUES (?)
            """
            cursor.execute(sql, (self.name,))
            conn.commit()
            self.id = cursor.lastrowid
        else:
            sql = """
                UPDATE authors
                SET name = ?
                WHERE id = ?
            """
            cursor.execute(sql, (self.name, self.id))
            conn.commit()

    @classmethod
    def instance_from_db(cls, row):
        return cls(row[0], row[1])

    @classmethod
    def get_all_authors(cls, cursor=default_cursor):
        sql = """
            SELECT *
            FROM authors
        """
        rows = cursor.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS authors
        """
        cursor.execute(sql)
        conn.commit()

