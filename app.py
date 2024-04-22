import streamlit as st
from dotenv import load_dotenv
import os
import pandas as pd
from db import Database

load_dotenv()


# Function to fetch books based on user input
def fetch_books(search, filter_by, order_by):
    with Database(os.getenv('DATABASE_URL')) as pg:
        
        query = """
        SELECT * FROM books
        WHERE LOWER(name) LIKE LOWER(%s) OR LOWER(description) LIKE LOWER(%s)
        ORDER BY {} {}
        """.format(order_by, filter_by)
        params = ('%' + search + '%', '%' + search + '%')
        df = pd.read_sql_query(query, pg.con, params=params)
        pg.con.close()
        return df

# Streamlit User Interface
def main():
    st.title('Book Finder')

    # User input
    search_query = st.text_input('Search by name or description:')
    order = st.selectbox('Order by:', ['rating', 'price'])
    order_type = st.selectbox('Order type:', ['ASC', 'DESC'])
    filter_button = st.button('Search')

    # Display results
    if filter_button:
        books = fetch_books(search_query, order_type, order)
        st.write(books)

if __name__ == '__main__':
    main()