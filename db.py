import time
import psycopg2

class Database:
    def __init__(self, database_url) -> None:
        self.con = psycopg2.connect(database_url)
        self.cur = self.con.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()

    def create_table(self):
        q = """
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            rating SMALLINT,
            price NUMERIC(10, 2),
            description TEXT
        );
        """
        self.cur.execute(q)
        self.con.commit()

    def truncate_table(self):
        q = """
        TRUNCATE TABLE quotes
        """
        self.cur.execute(q)
        self.con.commit()
    
    def insert_quote(self, book):
        q = """
        INSERT INTO books (name, rating, price, description) VALUES (%s, %s, %s, %s)
        """
        self.cur.execute(q, (book['name'], book['rating'], book['price'], book['description']))
        self.con.commit()
    
    def insert_all_books(self, books):
        q = """
        INSERT INTO books (name, rating, price, description) VALUES (%s, %s, %s, %s)
        """
        psycopg2.extras.execute_batch(self.cur, q, books)
        self.con.commit()        