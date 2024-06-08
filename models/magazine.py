from models.conn import CONN,CURSOR

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

        #  # Create a new magazine record in the database
        # CURSOR.execute("INSERT INTO magazines (id,name, category) VALUES (?, ?)", (self.id,self.name, self.category))
        # CONN.commit()
        # self.id = CURSOR.lastrowid


    def __repr__(self):
        return f'<Magazine {self.name}>'
    

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self,id):
        if not isinstance(id,int):
            ValueError("Id must be of type int")
        self._id=id

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
             ValueError("Name must be of type str")
        if not (2 <= len(value) <= 16):
             ValueError("Name must be between 2 and 16 characters, inclusive")
        
        self._name=value

    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self,value):
        if not isinstance(value,str):
            ValueError("Category must be of type str")
        if len(value)==0:
            ValueError("Categories must be longer than 0 characters")

        self._category=value


    def articles(self):
        from models.article import Article
        sql="""
            SELECT articles.id,articles.title,articles.content,articles.author_id,articles.magazine_id
            FROM articles
            INNER JOIN magazines
            ON magazines.id = articles.magazine_id
            WHERE magazine.id = ? 
            """
        CURSOR.execute(sql,(self.id,))
        rows = CURSOR.fetchall()
        return [Article(row[0], row[1], row[2], row[3], row[4]) for row in rows]
    
    def contributors(self):
        from models.author import Author
        sql = """
        SELECT DISTINCT authors.id, authors.name
        FROM authors
        INNER JOIN articles 
        ON authors.id = articles.author_id
        INNER JOIN magazines
        ON magazines.id = articles.magazine_id
        WHERE magazine_id = ?
        """
        CURSOR.execute(sql, (self.id,))
        rows = CURSOR.fetchall()
        return [Author(row[0], row[1]) for row in rows]
    
    def article_titles(self):
        sql = """
        SELECT articles.title
        FROM articles
        INNER JOIN magazines 
        ON magazines.id = articles.magazine_id
        WHERE magazines.id = ?
        """
        CURSOR.execute(sql, (self.id,))
        rows = CURSOR.fetchall()
        if rows:
            return [row[0] for row in rows]
        else:
            return None
        
    def contributing_authors(self):
        from models.author import Author 
        sql = """
        SELECT authors.id, authors.name
        FROM authors
        INNER JOIN articles 
        ON authors.id = articles.author_id
        INNER JOIN magazines
        ON magazine.id = articles.magazine_id
        WHERE articles.magazine_id = ?
        GROUP BY authors.id, authors.name
        HAVING COUNT(articles.id) > 2
        """
        CURSOR.execute(sql, (self.id,))
        rows = CURSOR.fetchall()
        if rows:
            return [Author(row[0], row[1]) for row in rows]
        else:
            return None
        

    
