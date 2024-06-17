class Author:
    def __init__(self, id=None, name=None, conn=None, cursor=None):
        self.id = id
        self.name = name
        self.conn = conn
        self.cursor = cursor

    def __repr__(self):
        return f'<Author {self.name}>'

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int) and value is not None:
            raise TypeError("Id must be of type int")
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value) <= 0:
            raise ValueError("Name must be a non-empty string")
        self._name = value

    def save(self):
        if self.id is None:
            sql = "INSERT INTO authors (name) VALUES (?)"
            self.cursor.execute(sql, (self.name,))
            self.conn.commit()
            self.id = self.cursor.lastrowid
        else:
            sql = "UPDATE authors SET name = ? WHERE id = ?"
            self.cursor.execute(sql, (self.name, self.id))
            self.conn.commit()

    def magazines(self):
        from models.magazine import Magazine
        sql = """
        SELECT DISTINCT magazines.id, magazines.name, magazines.category
        FROM magazines
        JOIN articles ON magazines.id = articles.magazine_id
        WHERE articles.author_id = ?
        """
        self.cursor.execute(sql, (self.id,))
        rows = self.cursor.fetchall()
        return [Magazine(id=row[0], name=row[1], category=row[2], conn=self.conn, cursor=self.cursor) for row in rows]


    @classmethod
    def instance_from_db(cls, row, conn, cursor):
        return cls(row[0], row[1], conn=conn, cursor=cursor)

    @staticmethod
    def get_all_authors(conn, cursor):
        cursor.execute("SELECT id, name FROM authors")
        rows = cursor.fetchall()
        return [Author(name=row[1], conn=conn, cursor=cursor) for row in rows]
    
    @classmethod
    def drop_table(cls, conn, cursor):
        sql = """
            DROP TABLE IF EXISTS authors
        """
        cursor.execute(sql)
        conn.commit()
