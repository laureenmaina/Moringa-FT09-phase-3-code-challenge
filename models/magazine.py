from conn import CURSOR, CONN

class Magazine:
    def __init__(self, id=None, name=None, category=None):
        self.id = id
        self.name = name
        self.category = category

    def __repr__(self):
        return f'<Magazine {self.name}>'

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        if not isinstance(id, int) and id is not None:
            raise ValueError("Id must be of type int")
        self._id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Name must be of type str")
        if not (2 <= len(value) <= 16):
            raise ValueError("Name must be between 2 and 16 characters, inclusive")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str):
            raise ValueError("Category must be of type str")
        if len(value) == 0:
            raise ValueError("Category must be longer than 0 characters")
        self._category = value

    def articles(self):
        from models.article import Article
        sql = """
            SELECT articles.id, articles.title, articles.content, articles.author_id, articles.magazine_id
            FROM articles
            WHERE articles.magazine_id = ?
        """
        CURSOR.execute(sql, (self.id,))
        rows = CURSOR.fetchall()
        return [Article(row[0], row[1], row[2], row[3], row[4]) for row in rows]

    def contributors(self):
        from models.author import Author
        sql = """
            SELECT DISTINCT authors.id, authors.name
            FROM authors
            INNER JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        """
        CURSOR.execute(sql, (self.id,))
        rows = CURSOR.fetchall()
        return [Author(row[0], row[1]) for row in rows]

    def article_titles(self):
        sql = """
            SELECT articles.title
            FROM articles
            WHERE articles.magazine_id = ?
        """
        CURSOR.execute(sql, (self.id,))
        rows = CURSOR.fetchall()
        return [row[0] for row in rows] if rows else None

    def contributing_authors(self):
        from models.author import Author
        sql = """
            SELECT authors.id, authors.name
            FROM authors
            INNER JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id, authors.name
            HAVING COUNT(articles.id) > 2
        """
        CURSOR.execute(sql, (self.id,))
        rows = CURSOR.fetchall()
        return [Author(row[0], row[1]) for row in rows] if rows else None

    def save(self):
        if self.id is None:
            sql = """
                INSERT INTO magazines (name, category)
                VALUES (?, ?)
            """
            CURSOR.execute(sql, (self.name, self.category))
            CONN.commit()
            self.id = CURSOR.lastrowid
        else:
            sql = """
                UPDATE magazines
                SET name = ?, category = ?
                WHERE id = ?
            """
            CURSOR.execute(sql, (self.name, self.category, self.id))
            CONN.commit()


    @classmethod
    def instance_from_db(cls, row):
        return cls(row[0], row[1],row[2])

    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM magazines
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]
