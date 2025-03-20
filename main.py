import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with a refreshed, attractive color theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    
    html, body {
        background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header {
        font-size: 50px;
        font-weight: 700;
        color: #2F80ED;
        text-align: center;
        margin-bottom: 30px;
        padding-bottom: 10px;
        border-bottom: 3px solid #2F80ED;
    }
    
    .sub-header {
        font-size: 36px;
        font-weight: 600;
        color: #EB5757;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    
    .card {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 8px 16px rgba(47, 128, 237, 0.1);
        transition: transform 0.2s ease-in-out;
    }
    
    .card:hover {
        transform: translateY(-5px);
    }
    
    .book-title {
        font-size: 24px;
        font-weight: 700;
        color: #333333;
        margin-bottom: 8px;
    }
    
    .book-author {
        font-size: 20px;
        font-weight: 500;
        color: #555555;
        margin-bottom: 12px;
    }
    
    .book-details {
        font-size: 18px;
        color: #666666;
        margin-bottom: 6px;
    }
    
    .sidebar-content {
        background-color: #2F80ED;
        padding: 30px;
        border-radius: 15px;
        color: #ffffff;
        font-size: 20px;
    }
    
    .sidebar-content h2, .sidebar-content p {
        color: #ffffff;
    }
    
    .stButton button {
        background-color: #EB5757;
        color: #ffffff;
        font-weight: bold;
        border-radius: 8px;
        padding: 12px 24px;
        border: none;
        font-size: 18px;
    }
    
    .stButton button:hover {
        background-color: #cf4a4a;
    }
    
    .delete-btn {
        background-color: #D7263D !important;
    }
    
    .delete-btn:hover {
        background-color: #a31f2e !important;
    }
    
    .css-1d391kg {  /* Adjusts sidebar title font size */
        font-size: 22px;
        font-weight: 600;
    }
    
</style>
""", unsafe_allow_html=True)

# Initialize database
def init_db():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        genre TEXT,
        year INTEGER,
        isbn TEXT,
        description TEXT,
        cover_url TEXT,
        added_date TEXT
    )
    ''')
    conn.commit()
    
    # Check if we need to add sample books
    c.execute("SELECT COUNT(*) FROM books")
    count = c.fetchone()[0]
    
    if count == 0:
        # Add sample books
        sample_books = [
            ("To Kill a Mockingbird", "Harper Lee", "Fiction", 1960, "978-0061120084", 
             "A classic of modern American literature about racial inequality.", 
             f"/placeholder.svg?height=300&width=200&text=To+Kill+a+Mockingbird", 
             datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            
            ("1984", "George Orwell", "Dystopian", 1949, "978-0451524935", 
             "A dystopian social science fiction novel about totalitarianism.", 
             f"/placeholder.svg?height=300&width=200&text=1984", 
             datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            
            ("The Great Gatsby", "F. Scott Fitzgerald", "Classic", 1925, "978-0743273565", 
             "A novel about the American Dream set in the Roaring Twenties.", 
             f"/placeholder.svg?height=300&width=200&text=The+Great+Gatsby", 
             datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            
            ("Pride and Prejudice", "Jane Austen", "Romance", 1813, "978-0141439518", 
             "A romantic novel of manners that depicts the emotional development of Elizabeth Bennet.", 
             f"/placeholder.svg?height=300&width=200&text=Pride+and+Prejudice", 
             datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            
            ("The Hobbit", "J.R.R. Tolkien", "Fantasy", 1937, "978-0547928227", 
             "A fantasy novel about the adventures of hobbit Bilbo Baggins.", 
             f"/placeholder.svg?height=300&width=200&text=The+Hobbit", 
             datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        ]
        
        c.executemany('''
        INSERT INTO books (title, author, genre, year, isbn, description, cover_url, added_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_books)
        conn.commit()
    
    conn.close()

# Database operations
def get_all_books():
    conn = sqlite3.connect('library.db')
    books = pd.read_sql_query("SELECT * FROM books ORDER BY title", conn)
    conn.close()
    return books

def add_book(title, author, genre, year, isbn, description, cover_url):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('''
    INSERT INTO books (title, author, genre, year, isbn, description, cover_url, added_date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (title, author, genre, year, isbn, description, cover_url, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def update_book(id, title, author, genre, year, isbn, description, cover_url):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('''
    UPDATE books
    SET title = ?, author = ?, genre = ?, year = ?, isbn = ?, description = ?, cover_url = ?
    WHERE id = ?
    ''', (title, author, genre, year, isbn, description, cover_url, id))
    conn.commit()
    conn.close()

def delete_book(id):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def get_book(id):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("SELECT * FROM books WHERE id = ?", (id,))
    book = c.fetchone()
    conn.close()
    
    if book:
        return {
            "id": book[0],
            "title": book[1],
            "author": book[2],
            "genre": book[3],
            "year": book[4],
            "isbn": book[5],
            "description": book[6],
            "cover_url": book[7],
            "added_date": book[8]
        }
    return None

def search_books(query):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("""
    SELECT * FROM books 
    WHERE title LIKE ? OR author LIKE ? OR genre LIKE ? OR isbn LIKE ?
    ORDER BY title
    """, (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"))
    books = c.fetchall()
    conn.close()
    
    return pd.DataFrame(books, columns=["id", "title", "author", "genre", "year", "isbn", "description", "cover_url", "added_date"])

# Initialize the database
init_db()

# Sidebar for navigation with custom styling
st.sidebar.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
st.sidebar.markdown("## 📚 Navigation")
page = st.sidebar.radio("", ["View Books", "Add Book", "Edit/Delete Books", "Search Books"])
st.sidebar.markdown("</div>", unsafe_allow_html=True)

# Main content
st.markdown("<h1 class='main-header'>📚 Library Management System</h1>", unsafe_allow_html=True)

if page == "View Books":
    st.markdown("<h2 class='sub-header'>📖 Book Collection</h2>", unsafe_allow_html=True)
    
    books = get_all_books()
    
    # Display books in a grid without images
    cols = st.columns(3)
    for i, (_, book) in enumerate(books.iterrows()):
        with cols[i % 3]:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown(f"<p class='book-title'>{book['title']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='book-author'>by {book['author']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='book-details'>Genre: {book['genre']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='book-details'>Year: {book['year']}</p>", unsafe_allow_html=True)
            with st.expander("Description"):
                st.write(book['description'])
            st.markdown("</div>", unsafe_allow_html=True)

elif page == "Add Book":
    st.markdown("<h2 class='sub-header'>➕ Add New Book</h2>", unsafe_allow_html=True)
    
    with st.form("add_book_form"):
        title = st.text_input("Title", max_chars=100)
        author = st.text_input("Author", max_chars=100)
        genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Science Fiction", "Fantasy", 
                                       "Mystery", "Thriller", "Romance", "Biography", 
                                       "History", "Self-Help", "Other"])
        year = st.number_input("Publication Year", min_value=1000, max_value=datetime.now().year, 
                               value=2020, step=1)
        isbn = st.text_input("ISBN", max_chars=20)
        description = st.text_area("Description", height=150)
        
        # For demo purposes, we'll use a placeholder text for cover_url
        cover_url = f"/placeholder.svg?height=300&width=200&text={title.replace(' ', '+')}"
        
        submitted = st.form_submit_button("Add Book")
        
        if submitted:
            if title and author:
                add_book(title, author, genre, year, isbn, description, cover_url)
                st.success(f"Book '{title}' has been added successfully!")
                st.balloons()
            else:
                st.error("Title and Author are required fields.")

elif page == "Edit/Delete Books":
    st.markdown("<h2 class='sub-header'>✏️ Edit or Delete Books</h2>", unsafe_allow_html=True)
    
    books = get_all_books()
    if not books.empty:
        book_options = books['title'].tolist()
        selected_book_title = st.selectbox("Select a book to edit or delete", book_options)
        
        selected_book = books[books['title'] == selected_book_title].iloc[0]
        book_id = selected_book['id']
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f"<p class='book-title'>{selected_book['title']}</p>", unsafe_allow_html=True)
        
        with col2:
            with st.form("edit_book_form"):
                edit_title = st.text_input("Title", value=selected_book['title'], max_chars=100)
                edit_author = st.text_input("Author", value=selected_book['author'], max_chars=100)
                edit_genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Science Fiction", "Fantasy", 
                                                   "Mystery", "Thriller", "Romance", "Biography", 
                                                   "History", "Self-Help", "Other"], 
                                         index=["Fiction", "Non-Fiction", "Science Fiction", "Fantasy", 
                                                "Mystery", "Thriller", "Romance", "Biography", 
                                                "History", "Self-Help", "Other"].index(selected_book['genre']) 
                                                if selected_book['genre'] in ["Fiction", "Non-Fiction", "Science Fiction", "Fantasy", 
                                                                            "Mystery", "Thriller", "Romance", "Biography", 
                                                                            "History", "Self-Help", "Other"] else 0)
                edit_year = st.number_input("Publication Year", min_value=1000, max_value=datetime.now().year, 
                                           value=int(selected_book['year']), step=1)
                edit_isbn = st.text_input("ISBN", value=selected_book['isbn'] if selected_book['isbn'] else "", max_chars=20)
                edit_description = st.text_area("Description", value=selected_book['description'] if selected_book['description'] else "", height=150)
                
                # Update cover_url only if title changes
                if edit_title != selected_book['title']:
                    edit_cover_url = f"/placeholder.svg?height=300&width=200&text={edit_title.replace(' ', '+')}"
                else:
                    edit_cover_url = selected_book['cover_url']
                
                col1_btn, col2_btn = st.columns(2)
                with col1_btn:
                    update_button = st.form_submit_button("Update Book")
                with col2_btn:
                    delete_button = st.form_submit_button("Delete Book", type="primary", help="This action cannot be undone")
                
                if update_button:
                    if edit_title and edit_author:
                        update_book(book_id, edit_title, edit_author, edit_genre, edit_year, 
                                   edit_isbn, edit_description, edit_cover_url)
                        st.success(f"Book '{edit_title}' has been updated successfully!")
                    else:
                        st.error("Title and Author are required fields.")
                
                if delete_button:
                    delete_book(book_id)
                    st.success(f"Book '{selected_book['title']}' has been deleted successfully!")
                    st.experimental_rerun()
    else:
        st.info("No books in the library yet. Add some books first!")

elif page == "Search Books":
    st.markdown("<h2 class='sub-header'>🔍 Search Books</h2>", unsafe_allow_html=True)
    
    search_query = st.text_input("Search by title, author, genre, or ISBN")
    
    if search_query:
        results = search_books(search_query)
        
        if not results.empty:
            st.success(f"Found {len(results)} results for '{search_query}'")
            
            # Display search results without images
            cols = st.columns(3)
            for i, (_, book) in enumerate(results.iterrows()):
                with cols[i % 3]:
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.markdown(f"<p class='book-title'>{book['title']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p class='book-author'>by {book['author']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p class='book-details'>Genre: {book['genre']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p class='book-details'>Year: {book['year']}</p>", unsafe_allow_html=True)
                    with st.expander("Description"):
                        st.write(book['description'])
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning(f"No books found matching '{search_query}'")
    else:
        st.info("Enter a search term to find books in the library")

# Footer
st.markdown("---")
st.markdown("### 📚 Library Management System | Created with Streamlit and SQLite")
