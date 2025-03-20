import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import random

# Set page configuration
st.set_page_config(
    page_title="BookVerse | Modern Library System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with modern design and beautiful typography
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap');
    
    :root {
        --primary-color: #6C63FF;
        --secondary-color: #FF6584;
        --accent-color: #43B97F;
        --background-color: #F9F7FF;
        --card-color: #FFFFFF;
        --text-primary: #333333;
        --text-secondary: #666666;
        --text-tertiary: #999999;
        --shadow: rgba(108, 99, 255, 0.15);
    }
    
    .dark {
        --primary-color: #8F88FF;
        --secondary-color: #FF85A1;
        --accent-color: #5ED4A0;
        --background-color: #1E1E2E;
        --card-color: #2D2D44;
        --text-primary: #F0F0F0;
        --text-secondary: #CCCCCC;
        --text-tertiary: #999999;
        --shadow: rgba(0, 0, 0, 0.3);
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: var(--background-color);
        font-family: 'Montserrat', sans-serif;
        color: var(--text-primary);
        transition: all 0.3s ease;
    }
    
    /* Main header styling */
    .main-header {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 1.5rem 0;
        padding-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    /* Sub header styling */
    .sub-header {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        font-weight: 600;
        color: var(--primary-color);
        margin: 1.5rem 0;
        position: relative;
        display: inline-block;
    }
    
    .sub-header::after {
        content: "";
        position: absolute;
        bottom: -10px;
        left: 0;
        width: 60px;
        height: 4px;
        background: var(--secondary-color);
        border-radius: 2px;
    }
    
    /* Card styling with hover effects */
    .book-card {
        background-color: var(--card-color);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 20px var(--shadow);
        transition: all 0.3s ease;
        border-top: 5px solid var(--primary-color);
        position: relative;
        overflow: hidden;
    }
    
    .book-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 30px var(--shadow);
    }
    
    .book-card::before {
        content: "";
        position: absolute;
        top: 0;
        right: 0;
        width: 0;
        height: 0;
        border-style: solid;
        border-width: 0 50px 50px 0;
        border-color: transparent var(--primary-color) transparent transparent;
        opacity: 0.2;
    }
    
    /* Book title styling */
    .book-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
        line-height: 1.3;
    }
    
    /* Book author styling */
    .book-author {
        font-size: 1.1rem;
        font-weight: 500;
        color: var(--secondary-color);
        margin-bottom: 1rem;
        font-style: italic;
    }
    
    /* Book details styling */
    .book-details {
        font-size: 0.95rem;
        color: var(--text-secondary);
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
    }
    
    .book-details i {
        margin-right: 0.5rem;
        color: var(--accent-color);
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        background-color: var(--primary-color);
        color: white;
    }
    
    .badge-fiction {
        background-color: #6C63FF;
    }
    
    .badge-nonfiction {
        background-color: #43B97F;
    }
    
    .badge-scifi {
        background-color: #FF6584;
    }
    
    .badge-fantasy {
        background-color: #FFA94D;
    }
    
    .badge-mystery {
        background-color: #845EF7;
    }
    
    .badge-thriller {
        background-color: #F03E3E;
    }
    
    .badge-romance {
        background-color: #FF8ED4;
    }
    
    .badge-biography {
        background-color: #20C997;
    }
    
    .badge-history {
        background-color: #748FFC;
    }
    
    .badge-selfhelp {
        background-color: #9775FA;
    }
    
    .badge-other {
        background-color: #868E96;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(90deg, var(--primary-color), var(--primary-color) 70%);
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(108, 99, 255, 0.2);
    }
    
    .stButton button:hover {
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        box-shadow: 0 6px 15px rgba(108, 99, 255, 0.3);
        transform: translateY(-2px);
    }
    
    /* Delete button styling */
    .delete-btn {
        background: linear-gradient(90deg, #F03E3E, #E03131) !important;
        box-shadow: 0 4px 10px rgba(240, 62, 62, 0.2) !important;
    }
    
    .delete-btn:hover {
        background: linear-gradient(90deg, #E03131, #C92A2A) !important;
        box-shadow: 0 6px 15px rgba(240, 62, 62, 0.3) !important;
    }
    
    /* Form styling */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] div, .stNumberInput div[data-baseweb="input"] input {
        background-color: var(--card-color);
        border: 2px solid #E9ECEF;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-family: 'Montserrat', sans-serif;
        color: var(--text-primary);
        transition: all 0.2s ease;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox div[data-baseweb="select"] div:focus, .stNumberInput div[data-baseweb="input"] input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(108, 99, 255, 0.2);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: 600;
        color: var(--primary-color);
        background-color: var(--card-color);
        border-radius: 8px;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: var(--card-color);
        border-right: none;
        box-shadow: 5px 0 15px var(--shadow);
    }
    
    .sidebar-content {
        padding: 2rem 1rem;
    }
    
    .sidebar-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    .sidebar-subtitle {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--secondary-color);
        margin: 1.5rem 0 1rem 0;
    }
    
    /* Animation classes */
    .fade-in {
        animation: fadeIn 0.5s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Stats card styling */
    .stats-card {
        background-color: var(--card-color);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 10px 20px var(--shadow);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stats-card:hover {
        transform: translateY(-5px);
    }
    
    .stats-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }
    
    .stats-label {
        font-size: 1rem;
        color: var(--text-secondary);
    }
    
    /* Search box styling */
    .search-container {
        position: relative;
        margin-bottom: 2rem;
    }
    
    .search-icon {
        position: absolute;
        left: 1rem;
        top: 50%;
        transform: translateY(-50%);
        color: var(--text-tertiary);
    }
    
    .search-input {
        width: 100%;
        padding: 0.8rem 1rem 0.8rem 3rem;
        border-radius: 50px;
        border: 2px solid #E9ECEF;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .search-input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(108, 99, 255, 0.2);
        outline: none;
    }
    
    /* Empty state styling */
    .empty-state {
        text-align: center;
        padding: 3rem 0;
    }
    
    .empty-state-icon {
        font-size: 5rem;
        color: var(--text-tertiary);
        margin-bottom: 1.5rem;
    }
    
    .empty-state-text {
        font-size: 1.2rem;
        color: var(--text-secondary);
        margin-bottom: 2rem;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: var(--text-tertiary);
        font-size: 0.9rem;
    }
    
    .footer a {
        color: var(--primary-color);
        text-decoration: none;
    }
    
    /* Theme toggle */
    .theme-toggle {
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 1000;
        background-color: var(--card-color);
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 10px var(--shadow);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .theme-toggle:hover {
        transform: rotate(30deg);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--background-color);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-color);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-color);
    }
    
    /* Tooltip styling */
    .tooltip {
        position: relative;
        display: inline-block;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 120px;
        background-color: var(--primary-color);
        color: white;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -60px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    /* Option menu styling */
    .nav-link {
        font-weight: 600 !important;
        color: var(--text-primary) !important;
    }
    
    .nav-link.active {
        background-color: var(--primary-color) !important;
        color: white !important;
    }
    
    /* Book cover styling */
    .book-cover {
        width: 100%;
        height: 200px;
        background-color: var(--primary-color);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        text-align: center;
        padding: 10px;
        margin-bottom: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
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
        added_date TEXT
    )
    ''')
    conn.commit()
    
    # Check if we need to add sample books
    c.execute("SELECT COUNT(*) FROM books")
    count = c.fetchone()[0]
    
    if count == 0:
        # Add sample books with more details
        sample_books = [
            ("To Kill a Mockingbird", "Harper Lee", "Fiction", 1960, "978-0061120084", 
             "A classic of modern American literature about racial inequality in the American South.", 
             datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            
            ("1984", "George Orwell", "Dystopian", 1949, "978-0451524935", 
             "A dystopian social science fiction novel about totalitarianism, mass surveillance, and repressive regimentation.", 
             datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            
            ("The Great Gatsby", "F. Scott Fitzgerald", "Classic", 1925, "978-0743273565", 
             "A novel about the American Dream, decadence, resistance to change, and social upheaval set in the Roaring Twenties.", 
             datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            
            ("Pride and Prejudice", "Jane Austen", "Romance", 1813, "978-0141439518", 
             "A romantic novel of manners that depicts the emotional development of Elizabeth Bennet, who learns about the repercussions of hasty judgments.", 
             datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            
            ("The Hobbit", "J.R.R. Tolkien", "Fantasy", 1937, "978-0547928227", 
             "A fantasy novel about the adventures of hobbit Bilbo Baggins, who is hired by the wizard Gandalf as a burglar for a group of dwarves.", 
             datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            
            ("One Hundred Years of Solitude", "Gabriel García Márquez", "Magical Realism", 1967, "978-0060883287", 
             "A landmark of magical realism that tells the multi-generational story of the Buendía family in the fictional town of Macondo.", 
             datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            
            ("The Alchemist", "Paulo Coelho", "Fiction", 1988, "978-0062315007", 
             "A philosophical novel about a young Andalusian shepherd who dreams of finding worldly treasures and embarks on a journey to find them.", 
             datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            
            ("The Catcher in the Rye", "J.D. Salinger", "Coming-of-age", 1951, "978-0316769488", 
             "A novel about teenage angst, alienation, and the loss of innocence, narrated by the protagonist Holden Caulfield.", 
             datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            
            ("The Lord of the Rings", "J.R.R. Tolkien", "Fantasy", 1954, "978-0618640157", 
             "An epic high-fantasy novel that follows the quest to destroy the One Ring, which was created by the Dark Lord Sauron.", 
             datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            
            ("Crime and Punishment", "Fyodor Dostoevsky", "Psychological Fiction", 1866, "978-0143107637", 
             "A novel that focuses on the mental anguish and moral dilemmas of Rodion Raskolnikov, an impoverished ex-student in Saint Petersburg.", 
             datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        ]
        
        c.executemany('''
        INSERT INTO books (title, author, genre, year, isbn, description, added_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', sample_books)
        conn.commit()
    
    conn.close()

# Database operations
def get_all_books():
    conn = sqlite3.connect('library.db')
    books = pd.read_sql_query("SELECT * FROM books ORDER BY title", conn)
    conn.close()
    return books

def add_book(title, author, genre, year, isbn, description):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('''
    INSERT INTO books (title, author, genre, year, isbn, description, added_date)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (title, author, genre, year, isbn, description, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def update_book(id, title, author, genre, year, isbn, description):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('''
    UPDATE books
    SET title = ?, author = ?, genre = ?, year = ?, isbn = ?, description = ?
    WHERE id = ?
    ''', (title, author, genre, year, isbn, description, id))
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
            "added_date": book[7]
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
    
    return pd.DataFrame(books, columns=["id", "title", "author", "genre", "year", "isbn", "description", "added_date"])

def get_stats():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    
    # Total books
    c.execute("SELECT COUNT(*) FROM books")
    total_books = c.fetchone()[0]
    
    # Total authors
    c.execute("SELECT COUNT(DISTINCT author) FROM books")
    total_authors = c.fetchone()[0]
    
    # Genre distribution
    c.execute("SELECT genre, COUNT(*) FROM books GROUP BY genre ORDER BY COUNT(*) DESC")
    genre_data = c.fetchall()
    
    # Year distribution
    c.execute("SELECT year, COUNT(*) FROM books GROUP BY year ORDER BY year")
    year_data = c.fetchall()
    
    conn.close()
    
    return {
        "total_books": total_books,
        "total_authors": total_authors,
        "genre_data": genre_data,
        "year_data": year_data
    }

# Initialize the database
init_db()

# Generate a random color for book covers
def get_random_color():
    colors = [
        "#6C63FF", "#FF6584", "#43B97F", "#FFA94D", "#845EF7", 
        "#F03E3E", "#FF8ED4", "#20C997", "#748FFC", "#9775FA"
    ]
    return random.choice(colors)

# Main content
st.markdown("<h1 class='main-header'>📚 BookVerse</h1>", unsafe_allow_html=True)

# Create tabs
tabs = st.tabs(["📚 Browse", "➕ Add Book", "✏️ Edit Books", "🔍 Search", "📊 Statistics"])

with tabs[0]:  # Browse Books
    st.markdown("<h2 class='sub-header fade-in'>📖 Book Collection</h2>", unsafe_allow_html=True)
    
    books = get_all_books()
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        genre_filter = st.selectbox("Filter by Genre", ["All"] + sorted(books["genre"].unique().tolist()))
    with col2:
        sort_by = st.selectbox("Sort by", ["Title (A-Z)", "Title (Z-A)", "Author", "Year (Newest)", "Year (Oldest)"])
    
    # Apply filters
    if genre_filter != "All":
        filtered_books = books[books["genre"] == genre_filter]
    else:
        filtered_books = books
    
    # Apply sorting
    if sort_by == "Title (A-Z)":
        filtered_books = filtered_books.sort_values("title")
    elif sort_by == "Title (Z-A)":
        filtered_books = filtered_books.sort_values("title", ascending=False)
    elif sort_by == "Author":
        filtered_books = filtered_books.sort_values("author")
    elif sort_by == "Year (Newest)":
        filtered_books = filtered_books.sort_values("year", ascending=False)
    elif sort_by == "Year (Oldest)":
        filtered_books = filtered_books.sort_values("year")
    
    # Display books in a grid with cards
    if not filtered_books.empty:
        cols = st.columns(3)
        for i, (_, book) in enumerate(filtered_books.iterrows()):
            with cols[i % 3]:
                color = get_random_color()
                st.markdown(f"""
                <div class='book-card fade-in'>
                    <div class='book-cover' style='background-color: {color};'>
                        {book['title']}
                    </div>
                    <div class='book-title'>{book['title']}</div>
                    <div class='book-author'>by {book['author']}</div>
                    <div class='book-details'><i>📅</i> Published: {book['year']}</div>
                    <div class='badge badge-{book["genre"].lower().replace(" ", "")}'>{book['genre']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("Description"):
                    st.write(book['description'])
    else:
        st.info("No books found matching your criteria.")

with tabs[1]:  # Add Book
    st.markdown("<h2 class='sub-header fade-in'>➕ Add New Book</h2>", unsafe_allow_html=True)
    
    with st.form("add_book_form"):
        title = st.text_input("Title", max_chars=100)
        author = st.text_input("Author", max_chars=100)
        genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Science Fiction", "Fantasy", 
                                      "Mystery", "Thriller", "Romance", "Biography", 
                                      "History", "Self-Help", "Magical Realism", "Coming-of-age",
                                      "Psychological Fiction", "Other"])
        year = st.number_input("Publication Year", min_value=1000, max_value=datetime.now().year, 
                              value=2020, step=1)
        isbn = st.text_input("ISBN", max_chars=20)
        description = st.text_area("Description", height=150)
        
        submitted = st.form_submit_button("Add Book")
        
        if submitted:
            if title and author:
                add_book(title, author, genre, year, isbn, description)
                st.success(f"Book '{title}' has been added successfully!")
                st.balloons()
                
                # Show success card
                color = get_random_color()
                st.markdown(f"""
                <div class='book-card fade-in'>
                    <div class='book-cover' style='background-color: {color};'>
                        {title}
                    </div>
                    <div class='book-title'>{title}</div>
                    <div class='book-author'>by {author}</div>
                    <div class='book-details'><i>📅</i> Published: {year}</div>
                    <div class='badge badge-{genre.lower().replace(" ", "")}'>{genre}</div>
                    <p>Book added to your library!</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Title and Author are required fields.")

with tabs[2]:  # Edit Books
    st.markdown("<h2 class='sub-header fade-in'>✏️ Edit or Delete Books</h2>", unsafe_allow_html=True)
    
    books = get_all_books()
    if not books.empty:
        # Create a searchable dropdown
        book_options = books['title'].tolist()
        selected_book_title = st.selectbox("Select a book to edit or delete", book_options)
        
        selected_book = books[books['title'] == selected_book_title].iloc[0]
        book_id = selected_book['id']
        
        # Display book details in a card
        color = get_random_color()
        st.markdown(f"""
        <div class='book-card fade-in'>
            <div class='book-cover' style='background-color: {color};'>
                {selected_book['title']}
            </div>
            <div class='book-title'>{selected_book['title']}</div>
            <div class='book-author'>by {selected_book['author']}</div>
            <div class='book-details'><i>📅</i> Published: {selected_book['year']}</div>
            <div class='badge badge-{selected_book["genre"].lower().replace(" ", "")}'>{selected_book['genre']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("edit_book_form"):
            edit_title = st.text_input("Title", value=selected_book['title'], max_chars=100)
            edit_author = st.text_input("Author", value=selected_book['author'], max_chars=100)
            edit_genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Science Fiction", "Fantasy", 
                                              "Mystery", "Thriller", "Romance", "Biography", 
                                              "History", "Self-Help", "Magical Realism", "Coming-of-age",
                                              "Psychological Fiction", "Other"], 
                                     index=["Fiction", "Non-Fiction", "Science Fiction", "Fantasy", 
                                            "Mystery", "Thriller", "Romance", "Biography", 
                                            "History", "Self-Help", "Magical Realism", "Coming-of-age",
                                            "Psychological Fiction", "Other"].index(selected_book['genre']) 
                                            if selected_book['genre'] in ["Fiction", "Non-Fiction", "Science Fiction", "Fantasy", 
                                                                        "Mystery", "Thriller", "Romance", "Biography", 
                                                                        "History", "Self-Help", "Magical Realism", "Coming-of-age",
                                                                        "Psychological Fiction", "Other"] else 0)
            edit_year = st.number_input("Publication Year", min_value=1000, max_value=datetime.now().year, 
                                       value=int(selected_book['year']), step=1)
            edit_isbn = st.text_input("ISBN", value=selected_book['isbn'] if selected_book['isbn'] else "", max_chars=20)
            edit_description = st.text_area("Description", value=selected_book['description'] if selected_book['description'] else "", height=150)
            
            col1_btn, col2_btn = st.columns(2)
            with col1_btn:
                update_button = st.form_submit_button("Update Book")
            with col2_btn:
                delete_button = st.form_submit_button("Delete Book", type="primary", help="This action cannot be undone")
            
            if update_button:
                if edit_title and edit_author:
                    update_book(book_id, edit_title, edit_author, edit_genre, edit_year, 
                               edit_isbn, edit_description)
                    st.success(f"Book '{edit_title}' has been updated successfully!")
                else:
                    st.error("Title and Author are required fields.")
            
            if delete_button:
                delete_book(book_id)
                st.success(f"Book '{selected_book['title']}' has been deleted successfully!")
                st.experimental_rerun()
    else:
        # Empty state
        st.markdown("""
        <div class='empty-state'>
            <div class='empty-state-icon'>📚</div>
            <div class='empty-state-text'>No books in your library yet.</div>
            <p>Add some books to get started!</p>
        </div>
        """, unsafe_allow_html=True)

with tabs[3]:  # Search
    st.markdown("<h2 class='sub-header fade-in'>🔍 Search Books</h2>", unsafe_allow_html=True)
    
    # Create a stylish search box
    search_query = st.text_input("", placeholder="Search by title, author, genre, or ISBN...", 
                                help="Enter your search term and press Enter")
    
    if search_query:
        results = search_books(search_query)
        
        if not results.empty:
            st.success(f"Found {len(results)} results for '{search_query}'")
            
            # Display search results in cards
            cols = st.columns(3)
            for i, (_, book) in enumerate(results.iterrows()):
                with cols[i % 3]:
                    color = get_random_color()
                    st.markdown(f"""
                    <div class='book-card fade-in'>
                        <div class='book-cover' style='background-color: {color};'>
                            {book['title']}
                        </div>
                        <div class='book-title'>{book['title']}</div>
                        <div class='book-author'>by {book['author']}</div>
                        <div class='book-details'><i>📅</i> Published: {book['year']}</div>
                        <div class='badge badge-{book["genre"].lower().replace(" ", "")}'>{book['genre']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander("Description"):
                        st.write(book['description'])
        else:
            # No results found
            st.markdown("""
            <div class='empty-state'>
                <div class='empty-state-icon'>🔍</div>
                <div class='empty-state-text'>No books found matching your search.</div>
                <p>Try a different search term or browse all books.</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        # Search tips
        st.info("Enter a search term to find books in your library")
        
        st.markdown("""
        <div class='card'>
            <h3>Search Tips</h3>
            <ul>
                <li>Search by title: "Lord of the Rings"</li>
                <li>Search by author: "Tolkien"</li>
                <li>Search by genre: "Fantasy"</li>
                <li>Search by ISBN: "978-0"</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

with tabs[4]:  # Statistics
    st.markdown("<h2 class='sub-header fade-in'>📊 Library Statistics</h2>", unsafe_allow_html=True)
    
    # Get statistics
    stats = get_stats()
    
    # Display stats cards
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class='stats-card'>
            <div class='stats-number'>{stats['total_books']}</div>
            <div class='stats-label'>Total Books</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='stats-card'>
            <div class='stats-number'>{stats['total_authors']}</div>
            <div class='stats-label'>Unique Authors</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display genre distribution
    st.subheader("Genre Distribution")
    if stats['genre_data']:
        # Create a simple bar chart
        genre_df = pd.DataFrame(stats['genre_data'], columns=['Genre', 'Count'])
        st.bar_chart(genre_df.set_index('Genre'))
    
    # Display year distribution
    st.subheader("Publication Years")
    if stats['year_data']:
        # Create a simple line chart
        year_df = pd.DataFrame(stats['year_data'], columns=['Year', 'Count'])
        year_df['Year'] = year_df['Year'].astype(str)
        st.line_chart(year_df.set_index('Year'))

# Footer
st.markdown("---")
st.markdown("""
<div class='footer'>
    <p>📚 BookVerse | Modern Library Management System</p>
    <p>Created with ❤️ using Streamlit and SQLite</p>
</div>
""", unsafe_allow_html=True)