class Magazine:
    def __init__(self, id=None, name=None, category=None, conn=None, cursor=None):
        self.id = id
        self.name = name
        self.category = category
        self.conn = conn
        self.cursor = cursor

    def __repr__(self):
        return f'<Magazine {self.name}>'

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
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Name must be a non-empty string")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or len(value.strip()) == 0:
           raise ValueError("Category must be a non-empty string")
        self._category = value

    def save(self):
        if self.id is None:
            sql = "INSERT INTO magazines (name, category) VALUES (?, ?)"
            self.cursor.execute(sql, (self.name, self.category))
            self.id = self.cursor.lastrowid
        else:
            sql = "UPDATE magazines SET name = ?, category = ? WHERE id = ?"
            self.cursor.execute(sql, (self.name, self.category, self.id))
        self.conn.commit()

    def articles(self):
        from models.article import Article
        sql = "SELECT * FROM articles WHERE magazine_id = ?"
        self.cursor.execute(sql, (self.id,))
        rows = self.cursor.fetchall()
        return [Article(*row, conn=self.conn, cursor=self.cursor) for row in rows]

    def article_count(self):
        sql = "SELECT COUNT(*) FROM articles WHERE magazine_id = ?"
        self.cursor.execute(sql, (self.id,))
        return self.cursor.fetchone()[0]
    
    @classmethod
    def instance_from_db(cls, row, conn, cursor):
        return cls(row[0], row[1], row[2], conn=conn, cursor=cursor)

    @classmethod
    def get_all(cls, conn, cursor):
        sql = """
            SELECT *
            FROM magazines
        """
        rows = cursor.execute(sql).fetchall()
        return [cls.instance_from_db(row, conn, cursor) for row in rows]

    @classmethod
    def drop_table(cls, conn, cursor):
        sql = """
            DROP TABLE IF EXISTS magazines
        """
        cursor.execute(sql)
        conn.commit()
