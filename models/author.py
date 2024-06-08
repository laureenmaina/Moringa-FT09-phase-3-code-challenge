from models.conn import CONN,CURSOR

class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name

        # CURSOR.execute(
        #      "INSERT INTO authors(id,name) VALUES(?)",(self.name,))
        # CONN.commit()
        # self.id= CURSOR.lastrowid #Get the ID of the newly created author
       

    def __repr__(self):
        return f'<Author {self.name}>'
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self,value):
        if not isinstance(value,int):
            raise TypeError("Id must be of type int")
        self._id=value

    
    @property
    def name(self):
        if self._name:
            return self._name
        

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value)<=0:
                ValueError("Name must be a non-empty string")
        if not hasattr(self, '_name'):
                    self._name = value
        else:
                AttributeError("Name cannot be changed after instantiation")


    def articles(self):
        from models.article import Article
        sql="""
            SELECT articles.id,articles.title,articles.content,articles.author_id,articles.magazine_id
            FROM articles
            INNER JOIN authors
            ON authors.id = articles.author_id
            WHERE authors.id = ?
            """
        CURSOR.execute(sql, (self.id,))
        rows=CURSOR.fetchall()
        return [Article(row[0],row[1],row[2],row[3],row[4]) for row in rows]
        
    def magazines(self):
        from models.magazine import Magazine
        sql="""
            SELECT magazines.id,magazines.name,magazines.category
            FROM magazines
            INNER JOIN authors
            ON authors.id= articles.author_id
            WHERE author.id = ?
            """
        CURSOR.execute(sql, (self.id,))
        rows=CURSOR.fetchall()
        return [Magazine(row[0],row[1],row[2]) for row in rows]
       




