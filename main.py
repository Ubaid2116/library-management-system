import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import plotly.express as px
import extra_streamlit_components as stx
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests


# Set page configuration
st.set_page_config(
    page_title="BookVerse | Modern Library System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with modern design, animations and beautiful typography
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
    
    /* Lottie animation container */
    .lottie-container {
        display: flex;
        justify-content: center;
        margin: 1rem 0;
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
        rating REAL,
        pages INTEGER,
        language TEXT,
        added_date TEXT
    )
    ''')
    conn.commit()
    
    # Check if we need to add sample books
    c.execute("SELECT COUNT(*) FROM books")
    count = c.fetchone()[0]
    
    if count == 0:
        # Add sample books with more details
        languages = ["English", "Spanish", "French", "German", "Japanese"]
        sample_books = [
            ("To Kill a Mockingbird", "Harper Lee", "Fiction", 1960, "978-0061120084", 
             "A classic of modern American literature about racial inequality in the American South.", 
             f"/placeholder.svg?height=300&width=200&text=To+Kill+a+Mockingbird", 
             4.8, 281, "English", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            
            ("1984", "George Orwell", "Dystopian", 1949, "978-0451524935", 
             "A dystopian social science fiction novel about totalitarianism, mass surveillance, and repressive regimentation.", 
             f"/placeholder.svg?height=300&width=200&text=1984", 
             4.7, 328, "English", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            
            ("The Great Gatsby", "F. Scott Fitzgerald", "Classic", 1925, "978-0743273565", 
             "A novel about the American Dream, decadence, resistance to change, and social upheaval set in the Roaring Twenties.", 
             f"/placeholder.svg?height=300&width=200&text=The+Great+Gatsby", 
             4.5, 180, "English", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            
            ("Pride and Prejudice", "Jane Austen", "Romance", 1813, "978-0141439518", 
             "A romantic novel of manners that depicts the emotional development of Elizabeth Bennet, who learns about the repercussions of hasty judgments.", 
             f"/placeholder.svg?height=300&width=200&text=Pride+and+Prejudice", 
             4.6, 432, "English", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            
            ("The Hobbit", "J.R.R. Tolkien", "Fantasy", 1937, "978-0547928227", 
             "A fantasy novel about the adventures of hobbit Bilbo Baggins, who is hired by the wizard Gandalf as a burglar for a group of dwarves.", 
             f"/placeholder.svg?height=300&width=200&text=The+Hobbit", 
             4.9, 366, "English", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            
            ("One Hundred Years of Solitude", "Gabriel García Márquez", "Magical Realism", 1967, "978-0060883287", 
             "A landmark of magical realism that tells the multi-generational story of the Buendía family in the fictional town of Macondo.", 
             f"/placeholder.svg?height=300&width=200&text=One+Hundred+Years+of+Solitude", 
             4.7, 417, "Spanish", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            
            ("The Alchemist", "Paulo Coelho", "Fiction", 1988, "978-0062315007", 
             "A philosophical novel about a young Andalusian shepherd who dreams of finding worldly treasures and embarks on a journey to find them.", 
             f"/placeholder.svg?height=300&width=200&text=The+Alchemist", 
             4.6, 197, "Portuguese", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            
            ("The Catcher in the Rye", "J.D. Salinger", "Coming-of-age", 1951, "978-0316769488", 
             "A novel about teenage angst, alienation, and the loss of innocence, narrated by the protagonist Holden Caulfield.", 
             f"/placeholder.svg?height=300&width=200&text=The+Catcher+in+the+Rye", 
             4.3, 277, "English", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            
            ("The Lord of the Rings", "J.R.R. Tolkien", "Fantasy", 1954, "978-0618640157", 
             "An epic high-fantasy novel that follows the quest to destroy the One Ring, which was created by the Dark Lord Sauron.", 
             f"/placeholder.svg?height=300&width=200&text=The+Lord+of+the+Rings", 
             4.9, 1178, "English", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            
            ("Crime and Punishment", "Fyodor Dostoevsky", "Psychological Fiction", 1866, "978-0143107637", 
             "A novel that focuses on the mental anguish and moral dilemmas of Rodion Raskolnikov, an impoverished ex-student in Saint Petersburg.", 
             f"/placeholder.svg?height=300&width=200&text=Crime+and+Punishment", 
             4.5, 671, "Russian", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        ]
        
        c.executemany('''
        INSERT INTO books (title, author, genre, year, isbn, description, cover_url, rating, pages, language, added_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_books)
        conn.commit()
    
    conn.close()

# Database operations
def get_all_books():
    conn = sqlite3.connect('library.db')
    books = pd.read_sql_query("SELECT * FROM books ORDER BY title", conn)
    conn.close()
    return books

def add_book(title, author, genre, year, isbn, description, cover_url, rating=0, pages=0, language="English"):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('''
    INSERT INTO books (title, author, genre, year, isbn, description, cover_url, rating, pages, language, added_date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (title, author, genre, year, isbn, description, cover_url, rating, pages, language, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def update_book(id, title, author, genre, year, isbn, description, cover_url, rating, pages, language):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('''
    UPDATE books
    SET title = ?, author = ?, genre = ?, year = ?, isbn = ?, description = ?, cover_url = ?, rating = ?, pages = ?, language = ?
    WHERE id = ?
    ''', (title, author, genre, year, isbn, description, cover_url, rating, pages, language, id))
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
            "rating": book[8],
            "pages": book[9],
            "language": book[10],
            "added_date": book[11]
        }
    return None

def search_books(query):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("""
    SELECT * FROM books 
    WHERE title LIKE ? OR author LIKE ? OR genre LIKE ? OR isbn LIKE ? OR language LIKE ?
    ORDER BY title
    """, (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"))
    books = c.fetchall()
    conn.close()
    
    return pd.DataFrame(books, columns=["id", "title", "author", "genre", "year", "isbn", "description", "cover_url", "rating", "pages", "language", "added_date"])

def get_stats():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    
    # Total books
    c.execute("SELECT COUNT(*) FROM books")
    total_books = c.fetchone()[0]
    
    # Total authors
    c.execute("SELECT COUNT(DISTINCT author) FROM books")
    total_authors = c.fetchone()[0]
    
    # Average rating
    c.execute("SELECT AVG(rating) FROM books")
    avg_rating = c.fetchone()[0] or 0
    
    # Genre distribution
    c.execute("SELECT genre, COUNT(*) FROM books GROUP BY genre ORDER BY COUNT(*) DESC")
    genre_data = c.fetchall()
    
    # Language distribution
    c.execute("SELECT language, COUNT(*) FROM books GROUP BY language ORDER BY COUNT(*) DESC")
    language_data = c.fetchall()
    
    # Year distribution
    c.execute("SELECT year, COUNT(*) FROM books GROUP BY year ORDER BY year")
    year_data = c.fetchall()
    
    conn.close()
    
    return {
        "total_books": total_books,
        "total_authors": total_authors,
        "avg_rating": round(avg_rating, 1),
        "genre_data": genre_data,
        "language_data": language_data,
        "year_data": year_data
    }

# Initialize the database
init_db()

# Load Lottie animations
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Lottie animations
lottie_book = load_lottieurl('https://assets5.lottiefiles.com/packages/lf20_1cazwtnc.json')
lottie_add = load_lottieurl('https://assets2.lottiefiles.com/private_files/lf30_cp6h8mjh.json')
lottie_search = load_lottieurl('https://assets3.lottiefiles.com/packages/lf20_kqfglbhb.json')
lottie_stats = load_lottieurl('https://assets10.lottiefiles.com/packages/lf20_xlmz9xwm.json')

# Create tabs with option_menu
selected = option_menu(
    menu_title=None,
    options=["📚 Browse", "➕ Add Book", "✏️ Edit Books", "🔍 Search", "📊 Statistics"],
    icons=["book", "plus-circle", "pencil-square", "search", "bar-chart"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#f8f9fa", "border-radius": "10px", "margin-bottom": "20px"},
        "icon": {"color": "#6C63FF", "font-size": "16px"},
        "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "padding": "10px 20px", "--hover-color": "#f0f0f0"},
        "nav-link-selected": {"background-color": "#6C63FF", "color": "white"},
    }
)

# Main content
st.markdown("<h1 class='main-header'>📚 BookVerse</h1>", unsafe_allow_html=True)

# Create a cookie manager for theme toggle
cookie_manager = stx.CookieManager()
current_theme = cookie_manager.get(cookie="theme") or "light"

# Theme toggle button
if st.button("🌓 Toggle Theme"):
    current_theme = "dark" if current_theme == "light" else "light"
    cookie_manager.set("theme", current_theme, expires_at=datetime.now().timestamp() + 30*24*60*60)
    st.experimental_rerun()

# Apply theme class based on cookie
if current_theme == "dark":
    st.markdown("""
    <script>
        document.body.classList.add('dark');
    </script>
    """, unsafe_allow_html=True)

if selected == "📚 Browse":
    st.markdown("<h2 class='sub-header fade-in'>📖 Book Collection</h2>", unsafe_allow_html=True)
    
    # Lottie animation
    with st.container():
        st.markdown("<div class='lottie-container'>", unsafe_allow_html=True)
        st_lottie(lottie_book, height=200, key="book_animation")
        st.markdown("</div>", unsafe_allow_html=True)
    
    books = get_all_books()
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        genre_filter = st.selectbox("Filter by Genre", ["All"] + sorted(books["genre"].unique().tolist()))
    with col2:
        sort_by = st.selectbox("Sort by", ["Title (A-Z)", "Title (Z-A)", "Author", "Year (Newest)", "Year (Oldest)", "Rating (Highest)"])
    with col3:
        view_type = st.radio("View", ["Cards", "Table"], horizontal=True)
    
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
    elif sort_by == "Rating (Highest)":
        filtered_books = filtered_books.sort_values("rating", ascending=False)
    
    # Display books based on view type
    if view_type == "Cards":
        # Display books in a grid with cards
        cols = st.columns(3)
        for i, (_, book) in enumerate(filtered_books.iterrows()):
            with cols[i % 3]:
                st.markdown(f"""
                <div class='book-card fade-in'>
                    <div class='book-title'>{book['title']}</div>
                    <div class='book-author'>by {book['author']}</div>
                    <div class='book-details'><i>📅</i> Published: {book['year']}</div>
                    <div class='book-details'><i>⭐</i> Rating: {book['rating']}/5.0</div>
                    <div class='book-details'><i>📘</i> Pages: {book['pages']}</div>
                    <div class='book-details'><i>🌐</i> Language: {book['language']}</div>
                    <div class='badge badge-{book["genre"].lower().replace(" ", "")}'>{book['genre']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("Description"):
                    st.write(book['description'])
    else:
        # Display as table
        display_cols = ["title", "author", "genre", "year", "rating", "language"]
        st.dataframe(filtered_books[display_cols], use_container_width=True)

elif selected == "➕ Add Book":
    st.markdown("<h2 class='sub-header fade-in'>➕ Add New Book</h2>", unsafe_allow_html=True)
    
    # Lottie animation
    with st.container():
        st.markdown("<div class='lottie-container'>", unsafe_allow_html=True)
        st_lottie(lottie_add, height=200, key="add_animation")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Create tabs for basic and advanced info
    tab1, tab2 = st.tabs(["📝 Basic Info", "🔍 Advanced Details"])
    
    with tab1:
        with st.form("add_book_form_basic"):
            title = st.text_input("Title", max_chars=100)
            author = st.text_input("Author", max_chars=100)
            genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Science Fiction", "Fantasy", 
                                        "Mystery", "Thriller", "Romance", "Biography", 
                                        "History", "Self-Help", "Magical Realism", "Coming-of-age",
                                        "Psychological Fiction", "Other"])
            year = st.number_input("Publication Year", min_value=1000, max_value=datetime.now().year, 
                                value=2020, step=1)
            description = st.text_area("Description", height=150)
            
            col1, col2 = st.columns(2)
            with col1:
                rating = st.slider("Rating", 0.0, 5.0, 4.0, 0.1)
            with col2:
                language = st.selectbox("Language", ["English", "Spanish", "French", "German", "Italian", 
                                                    "Portuguese", "Russian", "Japanese", "Chinese", "Other"])
            
            # For demo purposes, we'll use a placeholder image
            cover_url = f"/placeholder.svg?height=300&width=200&text={title.replace(' ', '+')}"
            
            submitted_basic = st.form_submit_button("Add Book")
    
    with tab2:
        with st.form("add_book_form_advanced"):
            isbn = st.text_input("ISBN", max_chars=20)
            pages = st.number_input("Number of Pages", min_value=1, max_value=10000, value=300)
            
            # Additional fields could be added here
            publisher = st.text_input("Publisher (Optional)")
            edition = st.text_input("Edition (Optional)")
            
            submitted_advanced = st.form_submit_button("Add Book with Advanced Details")
    
    # Process form submission
    if submitted_basic:
        if title and author:
            add_book(title, author, genre, year, "", description, cover_url, rating, 0, language)
            st.success(f"Book '{title}' has been added successfully!")
            st.balloons()
            
            # Show success card
            st.markdown(f"""
            <div class='book-card fade-in'>
                <div class='book-title'>{title}</div>
                <div class='book-author'>by {author}</div>
                <div class='book-details'><i>📅</i> Published: {year}</div>
                <div class='book-details'><i>⭐</i> Rating: {rating}/5.0</div>
                <div class='badge badge-{genre.lower().replace(" ", "")}'>{genre}</div>
                <p>Book added to your library!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Title and Author are required fields.")
    
    if submitted_advanced:
        if title and author:
            add_book(title, author, genre, year, isbn, description, cover_url, rating, pages, language)
            st.success(f"Book '{title}' has been added successfully with advanced details!")
            st.balloons()
        else:
            st.error("Title and Author are required fields.")

elif selected == "✏️ Edit Books":
    st.markdown("<h2 class='sub-header fade-in'>✏️ Edit or Delete Books</h2>", unsafe_allow_html=True)
    
    books = get_all_books()
    if not books.empty:
        # Create a searchable dropdown
        book_options = books['title'].tolist()
        selected_book_title = st.selectbox("Select a book to edit or delete", book_options)
        
        selected_book = books[books['title'] == selected_book_title].iloc[0]
        book_id = selected_book['id']
        
        # Display book details in a card
        st.markdown(f"""
        <div class='book-card fade-in'>
            <div class='book-title'>{selected_book['title']}</div>
            <div class='book-author'>by {selected_book['author']}</div>
            <div class='book-details'><i>📅</i> Published: {selected_book['year']}</div>
            <div class='book-details'><i>⭐</i> Rating: {selected_book['rating']}/5.0</div>
            <div class='book-details'><i>📘</i> Pages: {selected_book['pages']}</div>
            <div class='book-details'><i>🌐</i> Language: {selected_book['language']}</div>
            <div class='badge badge-{selected_book["genre"].lower().replace(" ", "")}'>{selected_book['genre']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Create tabs for editing
        tab1, tab2 = st.tabs(["📝 Basic Info", "🔍 Advanced Details"])
        
        with tab1:
            with st.form("edit_book_form_basic"):
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
                edit_description = st.text_area("Description", value=selected_book['description'] if selected_book['description'] else "", height=150)
                
                col1, col2 = st.columns(2)
                with col1:
                    edit_rating = st.slider("Rating", 0.0, 5.0, float(selected_book['rating']), 0.1)
                with col2:
                    edit_language = st.selectbox("Language", ["English", "Spanish", "French", "German", "Italian", 
                                                            "Portuguese", "Russian", "Japanese", "Chinese", "Other"],
                                                index=["English", "Spanish", "French", "German", "Italian", 
                                                    "Portuguese", "Russian", "Japanese", "Chinese", "Other"].index(selected_book['language'])
                                                    if selected_book['language'] in ["English", "Spanish", "French", "German", "Italian", 
                                                                                    "Portuguese", "Russian", "Japanese", "Chinese", "Other"] else 0)
                
                update_button = st.form_submit_button("Update Book")
        
        with tab2:
            with st.form("edit_book_form_advanced"):
                edit_isbn = st.text_input("ISBN", value=selected_book['isbn'] if selected_book['isbn'] else "", max_chars=20)
                edit_pages = st.number_input("Number of Pages", min_value=1, max_value=10000, value=int(selected_book['pages']) if selected_book['pages'] else 300)
                
                # Keep the same cover or generate a new one if title changes
                if edit_title != selected_book['title']:
                    edit_cover_url = f"/placeholder.svg?height=300&width=200&text={edit_title.replace(' ', '+')}"
                else:
                    edit_cover_url = selected_book['cover_url']
                
                update_advanced_button = st.form_submit_button("Update Advanced Details")
        
        # Delete button outside of forms
        if st.button("Delete Book", type="primary", help="This action cannot be undone"):
            delete_book(book_id)
            st.success(f"Book '{selected_book['title']}' has been deleted successfully!")
            st.experimental_rerun()
        
        # Process form submissions
        if update_button:
            if edit_title and edit_author:
                # Keep advanced details the same
                update_book(book_id, edit_title, edit_author, edit_genre, edit_year, 
                        selected_book['isbn'], edit_description, selected_book['cover_url'], 
                        edit_rating, selected_book['pages'], edit_language)
                st.success(f"Book '{edit_title}' has been updated successfully!")
            else:
                st.error("Title and Author are required fields.")
        
        if update_advanced_button:
            if edit_title and edit_author:
                update_book(book_id, edit_title, edit_author, edit_genre, edit_year, 
                        edit_isbn, edit_description, edit_cover_url, 
                        edit_rating, edit_pages, edit_language)
                st.success(f"Book '{edit_title}' has been updated with advanced details!")
            else:
                st.error("Title and Author are required fields.")
    else:
        # Empty state
        st.markdown("""
        <div class='empty-state'>
            <div class='empty-state-icon'>📚</div>
            <div class='empty-state-text'>No books in your library yet.</div>
            <p>Add some books to get started!</p>
        </div>
        """, unsafe_allow_html=True)

elif selected == "🔍 Search":
    st.markdown("<h2 class='sub-header fade-in'>🔍 Search Books</h2>", unsafe_allow_html=True)
    
    # Lottie animation
    with st.container():
        st.markdown("<div class='lottie-container'>", unsafe_allow_html=True)
        st_lottie(lottie_search, height=200, key="search_animation")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Create a stylish search box
    search_query = st.text_input("", placeholder="Search by title, author, genre, ISBN or language...", 
                                help="Enter your search term and press Enter")
    
    if search_query:
        results = search_books(search_query)
        
        if not results.empty:
            st.success(f"Found {len(results)} results for '{search_query}'")
            
            # Display search results in cards
            cols = st.columns(3)
            for i, (_, book) in enumerate(results.iterrows()):
                with cols[i % 3]:
                    st.markdown(f"""
                    <div class='book-card fade-in'>
                        <div class='book-title'>{book['title']}</div>
                        <div class='book-author'>by {book['author']}</div>
                        <div class='book-details'><i>📅</i> Published: {book['year']}</div>
                        <div class='book-details'><i>⭐</i> Rating: {book['rating']}/5.0</div>
                        <div class='book-details'><i>📘</i> Pages: {book['pages']}</div>
                        <div class='book-details'><i>🌐</i> Language: {book['language']}</div>
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
                <li>Search by language: "Spanish"</li>
                <li>Search by ISBN: "978-0"</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif selected == "📊 Statistics":
    st.markdown("<h2 class='sub-header fade-in'>📊 Library Statistics</h2>", unsafe_allow_html=True)
    
    # Lottie animation
    with st.container():
        st.markdown("<div class='lottie-container'>", unsafe_allow_html=True)
        st_lottie(lottie_stats, height=200, key="stats_animation")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Get statistics
    stats = get_stats()
    
    # Display stats cards
    col1, col2, col3 = st.columns(3)
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
    
    with col3:
        st.markdown(f"""
        <div class='stats-card'>
            <div class='stats-number'>{stats['avg_rating']}</div>
            <div class='stats-label'>Average Rating</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Create charts
    st.subheader("Genre Distribution")
    if stats['genre_data']:
        genre_df = pd.DataFrame(stats['genre_data'], columns=['Genre', 'Count'])
        fig_genre = px.pie(genre_df, values='Count', names='Genre', hole=0.4,
                          color_discrete_sequence=px.colors.qualitative.Bold)
        fig_genre.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_genre, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Language Distribution")
        if stats['language_data']:
            language_df = pd.DataFrame(stats['language_data'], columns=['Language', 'Count'])
            fig_language = px.bar(language_df, x='Language', y='Count', 
                                color='Count', color_continuous_scale='Viridis')
            fig_language.update_layout(margin=dict(t=30, b=0, l=0, r=0))
            st.plotly_chart(fig_language, use_container_width=True)
    
    with col2:
        st.subheader("Publication Years")
        if stats['year_data']:
            year_df = pd.DataFrame(stats['year_data'], columns=['Year', 'Count'])
            fig_year = px.line(year_df, x='Year', y='Count', markers=True)
            fig_year.update_layout(margin=dict(t=30, b=0, l=0, r=0))
            st.plotly_chart(fig_year, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div class='footer'>
    <p>📚 BookVerse | Modern Library Management System</p>
    <p>Created with ❤️ using Streamlit, SQLite, and modern UI components</p>
</div>
""", unsafe_allow_html=True)