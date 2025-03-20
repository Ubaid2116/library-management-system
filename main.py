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

# Custom CSS with minimalist elegant design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Playfair+Display:wght@500;600;700;800&display=swap');
    
    :root {
        --primary-color: #4F46E5;
        --primary-light: #818CF8;
        --primary-dark: #3730A3;
        --secondary-color: #F43F5E;
        --accent-color: #10B981;
        --background-color: #F9FAFB;
        --card-color: #FFFFFF;
        --text-primary: #1F2937;
        --text-secondary: #4B5563;
        --text-tertiary: #9CA3AF;
        --shadow: rgba(0, 0, 0, 0.05);
        --shadow-hover: rgba(0, 0, 0, 0.1);
        --border-color: #E5E7EB;
        --gradient-primary: linear-gradient(135deg, #4F46E5, #818CF8);
        --gradient-secondary: linear-gradient(135deg, #F43F5E, #FB7185);
    }
    
    /* Dark mode variables */
    .dark {
        --primary-color: #818CF8;
        --primary-light: #A5B4FC;
        --primary-dark: #4F46E5;
        --secondary-color: #FB7185;
        --accent-color: #34D399;
        --background-color: #111827;
        --card-color: #1F2937;
        --text-primary: #F9FAFB;
        --text-secondary: #E5E7EB;
        --text-tertiary: #9CA3AF;
        --shadow: rgba(0, 0, 0, 0.2);
        --shadow-hover: rgba(0, 0, 0, 0.3);
        --border-color: #374151;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: var(--background-color);
        font-family: 'Poppins', sans-serif;
        color: var(--text-primary);
        transition: all 0.3s ease;
    }
    
    /* Main header styling */
    .main-header {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: 800;
        color: var(--primary-color);
        text-align: center;
        margin: 2rem 0 3rem 0;
        letter-spacing: -0.5px;
        line-height: 1.2;
    }
    
    .main-header span {
        display: block;
        font-size: 1.2rem;
        font-weight: 400;
        font-family: 'Poppins', sans-serif;
        color: var(--text-secondary);
        letter-spacing: 2px;
        margin-top: 0.5rem;
        text-transform: uppercase;
    }
    
    /* Section header styling */
    .section-header {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-color);
        margin: 2rem 0;
        position: relative;
        display: inline-block;
        padding-bottom: 0.5rem;
    }
    
    .section-header::after {
        content: "";
        position: absolute;
        bottom: 0;
        left: 0;
        width: 60px;
        height: 3px;
        background: var(--secondary-color);
        border-radius: 1.5px;
    }
    
    /* Card styling */
    .book-card {
        background-color: var(--card-color);
        border-radius: 12px;
        padding: 1.75rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px var(--shadow);
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 1px solid var(--border-color);
        position: relative;
        overflow: hidden;
    }
    
    .book-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 24px var(--shadow-hover);
        border-color: var(--primary-light);
    }
    
    /* Book cover styling */
    .book-cover {
        width: 100%;
        height: 180px;
        background: var(--gradient-primary);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        font-size: 1.25rem;
        text-align: center;
        padding: 1rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        position: relative;
        overflow: hidden;
    }
    
    .book-cover::after {
        content: "📖";
        position: absolute;
        bottom: 8px;
        right: 8px;
        font-size: 1.5rem;
        opacity: 0.7;
    }
    
    /* Book title styling */
    .book-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.4rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
        line-height: 1.3;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
    }
    
    /* Book author styling */
    .book-author {
        font-size: 1rem;
        font-weight: 500;
        color: var(--secondary-color);
        margin-bottom: 1rem;
        font-style: italic;
    }
    
    /* Book details styling */
    .book-details {
        font-size: 0.95rem;
        font-weight: 500;
        color: var(--text-secondary);
        margin-bottom: 0.6rem;
        display: flex;
        align-items: center;
    }
    
    .book-details i {
        margin-right: 0.6rem;
        color: var(--primary-color);
        font-size: 1rem;
        flex-shrink: 0;
    }
    
    /* Badge styling */
    .badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.5rem;
        margin-top: 0.75rem;
        background-color: var(--primary-light);
        color: white;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Genre specific badges */
    .badge-fiction { background-color: #4F46E5; }
    .badge-nonfiction { background-color: #10B981; }
    .badge-scifi { background-color: #7C3AED; }
    .badge-fantasy { background-color: #F59E0B; }
    .badge-mystery { background-color: #8B5CF6; }
    .badge-thriller { background-color: #EF4444; }
    .badge-romance { background-color: #EC4899; }
    .badge-biography { background-color: #10B981; }
    .badge-history { background-color: #3B82F6; }
    .badge-selfhelp { background-color: #8B5CF6; }
    .badge-other { background-color: #6B7280; }
    
    /* Button styling */
    .stButton button {
        background-color: var(--primary-color);
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.7rem 1.2rem;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 8px rgba(79, 70, 229, 0.2);
        width: 100%;
        text-transform: uppercase;
        font-size: 0.875rem;
        letter-spacing: 0.5px;
    }
    
    .stButton button:hover {
        background-color: var(--primary-dark);
        box-shadow: 0 6px 12px rgba(79, 70, 229, 0.3);
        transform: translateY(-2px);
    }
    
    /* Delete button styling */
    .delete-btn {
        background-color: #EF4444 !important;
        box-shadow: 0 4px 8px rgba(239, 68, 68, 0.2) !important;
    }
    
    .delete-btn:hover {
        background-color: #DC2626 !important;
        box-shadow: 0 6px 12px rgba(239, 68, 68, 0.3) !important;
    }
    
    /* Form styling */
    .stTextInput input, .stTextArea textarea, .stNumberInput div[data-baseweb="input"] input {
        background-color: var(--card-color);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 0.8rem 1rem;
        font-family: 'Poppins', sans-serif;
        font-weight: 400;
        color: var(--text-primary);
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px var(--shadow);
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus, .stNumberInput div[data-baseweb="input"] input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2);
    }
    
    /* Select box styling */
    .stSelectbox div[data-baseweb="select"] {
        background-color: var(--card-color);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        box-shadow: 0 2px 4px var(--shadow);
        transition: all 0.3s ease;
    }
    
    .stSelectbox div[data-baseweb="select"]:hover,
    .stSelectbox div[data-baseweb="select"]:focus-within {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2);
    }
    
    /* Filter container styling */
    .filter-container {
        background-color: var(--card-color);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px var(--shadow);
        border: 1px solid var(--border-color);
    }
    
    .filter-title {
        font-weight: 600;
        color: var(--primary-color);
        font-size: 1.1rem;
        margin-bottom: 1.25rem;
        display: flex;
        align-items: center;
    }
    
    .filter-title svg {
        margin-right: 0.5rem;
        color: var(--primary-color);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: 600;
        color: var(--primary-color);
        background-color: var(--card-color);
        border-radius: 8px;
        padding: 0.6rem 1rem;
        border: 1px solid var(--border-color);
    }
    
    /* Animation classes */
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Stats card styling */
    .stats-card {
        background-color: var(--card-color);
        border-radius: 12px;
        padding: 1.75rem;
        box-shadow: 0 4px 12px var(--shadow);
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid var(--border-color);
        border-left: 4px solid var(--primary-color);
    }
    
    .stats-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 8px 16px var(--shadow-hover);
    }
    
    .stats-card.accent {
        border-left-color: var(--secondary-color);
    }
    
    .stats-number {
        font-size: 2.75rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }
    
    .stats-card.accent .stats-number {
        color: var(--secondary-color);
    }
    
    .stats-label {
        font-size: 1rem;
        font-weight: 500;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Search styling */
    .search-container {
        position: relative;
        margin-bottom: 1.5rem;
    }
    
    .search-input {
        width: 100%;
        border: 1px solid var(--border-color);
        border-radius: 30px;
        padding: 0.75rem 1rem 0.75rem 3rem;
        font-family: 'Poppins', sans-serif;
        font-size: 1rem;
        color: var(--text-primary);
        background-color: var(--card-color);
        box-shadow: 0 2px 8px var(--shadow);
        transition: all 0.3s ease;
    }
    
    .search-input:focus {
        outline: none;
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2);
    }
    
    .search-icon {
        position: absolute;
        left: 1.25rem;
        top: 50%;
        transform: translateY(-50%);
        color: var(--text-tertiary);
    }
    
    /* Empty state styling */
    .empty-state {
        text-align: center;
        padding: 3rem 2rem;
        background-color: var(--card-color);
        border-radius: 12px;
        box-shadow: 0 4px 12px var(--shadow);
        margin: 2rem 0;
        border: 1px solid var(--border-color);
    }
    
    .empty-state-icon {
        font-size: 4rem;
        color: var(--primary-color);
        margin-bottom: 1.5rem;
        opacity: 0.7;
    }
    
    .empty-state-text {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-secondary);
        margin-bottom: 1rem;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 2.5rem 0;
        color: var(--text-tertiary);
        font-size: 0.875rem;
        font-weight: 400;
        margin-top: 3rem;
    }
    
    .footer-brand {
        font-weight: 600;
        font-size: 1rem;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        border-bottom: 1px solid var(--border-color);
        padding-bottom: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 6px;
        padding: 0.6rem 1rem;
        font-weight: 500;
        font-size: 0.95rem;
        color: var(--text-secondary);
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--primary-color);
        color: white;
        font-weight: 600;
    }
            
    .stTextInput input, 
    .stTextArea textarea, 
    .stNumberInput div[data-baseweb="input"] input,
    .stSelectbox div[data-baseweb="select"] {
        color: #000000 !important; /* Force black text color */
    }

    .stTextInput label, 
    .stTextArea label, 
    .stNumberInput label,
    .stSelectbox label {
        color: #000000 !important; /* Force black text color */
    }

    .stTextInput input::placeholder, 
    .stTextArea textarea::placeholder, 
    .stNumberInput div[data-baseweb="input"] input::placeholder {
        color: #666666 !important; /* Gray placeholder text */
    }
    
    /* Chart styling */
    [data-testid="stVegaLiteChart"] {
        background-color: var(--card-color);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px var(--shadow);
        border: 1px solid var(--border-color);
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

# Generate a random gradient for book covers
def get_random_cover_color():
    colors = [
        "#4F46E5", "#7C3AED", "#F43F5E", "#10B981",
        "#3B82F6", "#F59E0B", "#EC4899", "#8B5CF6"
    ]
    return random.choice(colors)

# Main content
st.markdown("<h1 class='main-header'>📚 BOOKVERSE<span>Personal Library Management</span></h1>", unsafe_allow_html=True)

# Create tabs with better styling
tabs = st.tabs(["📚 Browse", "➕ Add Book", "✏️ Edit Books", "🔍 Search", "📊 Statistics"])

with tabs[0]:  # Browse Books
    st.markdown("<h2 class='section-header fade-in'>Book Collection</h2>", unsafe_allow_html=True)
    
    books = get_all_books()
    
    # Filter options with completely redesigned styling
    st.markdown("""
    <div class="filter-container fade-in">
        <div class="filter-title">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon>
            </svg>
            Filter & Sort
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        genre_filter = st.selectbox("Filter by Genre", ["All"] + sorted(books["genre"].unique().tolist()), label_visibility="collapsed", key="genre_filter")
    with col2:
        sort_by = st.selectbox("Sort by", ["Title (A-Z)", "Title (Z-A)", "Author", "Year (Newest)", "Year (Oldest)"], label_visibility="collapsed", key="sort_by")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
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
    
    # Display books in a grid with enhanced cards
    if not filtered_books.empty:
        cols = st.columns(3)
        for i, (_, book) in enumerate(filtered_books.iterrows()):
            with cols[i % 3]:
                cover_color = get_random_cover_color()
                st.markdown(f"""
                <div class='book-card fade-in'>
                    <div class='book-cover' style='background-color: {cover_color};'>
                        {book['title']}
                    </div>
                    <div class='book-title'>{book['title']}</div>
                    <div class='book-author'>by {book['author']}</div>
                    <div class='book-details'><i>📅</i> {book['year']}</div>
                    <div class='book-details'><i>📚</i> {book['genre']}</div>
                    <div class='badge badge-{book["genre"].lower().replace(" ", "")}'>{book['genre']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("View Description"):
                    st.write(book['description'])
    else:
        st.markdown("""
        <div class='empty-state'>
            <div class='empty-state-icon'>📚</div>
            <div class='empty-state-text'>No books found</div>
            <p>Try adjusting your filters or add some books to your library.</p>
        </div>
        """, unsafe_allow_html=True)

with tabs[1]:  # Add Book
    st.markdown("<h2 class='section-header fade-in'>Add New Book</h2>", unsafe_allow_html=True)
    
    # Enhanced form with better styling
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
                
                # Show success card with enhanced styling
                cover_color = get_random_cover_color()
                st.markdown(f"""
                <div class='book-card fade-in'>
                    <div class='book-cover' style='background-color: {cover_color};'>
                        {title}
                    </div>
                    <div class='book-title'>{title}</div>
                    <div class='book-author'>by {author}</div>
                    <div class='book-details'><i>📅</i> {year}</div>
                    <div class='book-details'><i>📚</i> {genre}</div>
                    <div class='badge badge-{genre.lower().replace(" ", "")}'>{genre}</div>
                    <p style="font-weight: 600; color: #10B981; margin-top: 12px; font-size: 0.95rem;">✓ Successfully added to your library</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Title and Author are required fields.")

with tabs[2]:  # Edit Books
    st.markdown("<h2 class='section-header fade-in'>Manage Your Books</h2>", unsafe_allow_html=True)
    
    books = get_all_books()
    if not books.empty:
        # Searchable dropdown
        st.markdown("""
        <div class="filter-container fade-in">
            <div class="filter-title">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                    <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
                </svg>
                Select a Book to Edit
            </div>
        """, unsafe_allow_html=True)
        
        book_options = books['title'].tolist()
        selected_book_title = st.selectbox("Select Book", book_options, label_visibility="collapsed", key="edit_book_select")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        selected_book = books[books['title'] == selected_book_title].iloc[0]
        book_id = selected_book['id']
        
        # Display book details
        cover_color = get_random_cover_color()
        st.markdown(f"""
        <div class='book-card fade-in'>
            <div class='book-cover' style='background-color: {cover_color};'>
                {selected_book['title']}
            </div>
            <div class='book-title'>{selected_book['title']}</div>
            <div class='book-author'>by {selected_book['author']}</div>
            <div class='book-details'><i>📅</i> {selected_book['year']}</div>
            <div class='book-details'><i>📚</i> {selected_book['genre']}</div>
            <div class='badge badge-{selected_book["genre"].lower().replace(" ", "")}'>{selected_book['genre']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Edit form
        with st.form("edit_book_form"):
            st.markdown("<p style='font-weight: 600; color: var(--primary-color); margin-bottom: 1rem; font-size: 1.1rem;'>Edit Book Details</p>", unsafe_allow_html=True)
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
            
            update_button = st.form_submit_button("Update Book")
            
            if update_button:
                if edit_title and edit_author:
                    update_book(book_id, edit_title, edit_author, edit_genre, edit_year, 
                               edit_isbn, edit_description)
                    st.success(f"Book '{edit_title}' has been updated successfully!")
                else:
                    st.error("Title and Author are required fields.")
        
        # Separate delete section
        st.markdown("<hr style='margin: 2rem 0;' />", unsafe_allow_html=True)
        st.markdown("<h3 style='font-weight: 600; color: var(--secondary-color);'>Delete Book</h3>", unsafe_allow_html=True)
        st.warning("This action cannot be undone.")
        
        if st.button("Delete Book", type="primary"):
            st.session_state['show_confirm'] = True
        
        if 'show_confirm' in st.session_state and st.session_state['show_confirm']:
            st.markdown("<p style='font-weight: 600; color: var(--secondary-color);'>Are you sure you want to delete this book?</p>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Yes, delete it"):
                    delete_book(book_id)
                    st.success(f"Book '{selected_book['title']}' has been deleted successfully!")
                    del st.session_state['show_confirm']
                    st.rerun()
            with col2:
                if st.button("Cancel"):
                    del st.session_state['show_confirm']
                    st.rerun()
    else:
        st.markdown("""
        <div class='empty-state'>
            <div class='empty-state-icon'>📚</div>
            <div class='empty-state-text'>Your library is empty</div>
            <p style="font-weight: 500; font-size: 0.95rem; color: var(--text-secondary);">Add some books to get started!</p>
        </div>
        """, unsafe_allow_html=True)
        
with tabs[3]:  # Search
    st.markdown("<h2 class='section-header fade-in'>Search Your Library</h2>", unsafe_allow_html=True)
    
    # Enhanced search box
    st.markdown("""
    <div class="filter-container fade-in">
        <div class="filter-title">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
            Find Books
        </div>
    """, unsafe_allow_html=True)
    
    search_query = st.text_input("Search", placeholder="Search by title, author, genre, or ISBN...", 
                                help="Enter your search term and press Enter", label_visibility="collapsed", key="search_input")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if search_query:
        results = search_books(search_query)
        
        if not results.empty:
            st.success(f"Found {len(results)} results for '{search_query}'")
            
            # Display search results in enhanced cards
            cols = st.columns(3)
            for i, (_, book) in enumerate(results.iterrows()):
                with cols[i % 3]:
                    cover_color = get_random_cover_color()
                    st.markdown(f"""
                    <div class='book-card fade-in'>
                        <div class='book-cover' style='background-color: {cover_color};'>
                            {book['title']}
                        </div>
                        <div class='book-title'>{book['title']}</div>
                        <div class='book-author'>by {book['author']}</div>
                        <div class='book-details'><i>📅</i> {book['year']}</div>
                        <div class='book-details'><i>📚</i> {book['genre']}</div>
                        <div class='badge badge-{book["genre"].lower().replace(" ", "")}'>{book['genre']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander("View Description"):
                        st.write(book['description'])
        else:
            # Enhanced empty search results
            st.markdown("""
            <div class='empty-state'>
                <div class='empty-state-icon'>🔍</div>
                <div class='empty-state-text'>No matching books found</div>
                <p style="font-weight: 500; font-size: 0.95rem; color: var(--text-secondary);">Try a different search term or browse all books.</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        # Enhanced search tips
        st.markdown("""
        <div style="background-color: var(--card-color); border-radius: 12px; padding: 1.5rem; box-shadow: 0 4px 12px var(--shadow); margin-top: 1.5rem; border: 1px solid var(--border-color);">
            <h3 style="font-weight: 600; color: var(--primary-color); margin-bottom: 1rem; font-size: 1.1rem;">Search Tips</h3>
            <ul style="font-weight: 500; font-size: 0.95rem; color: var(--text-secondary); margin-left: 1.5rem; line-height: 1.8;">
                <li>Search by title: "Lord of the Rings"</li>
                <li>Search by author: "Tolkien"</li>
                <li>Search by genre: "Fantasy"</li>
                <li>Search by ISBN: "978-0"</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

with tabs[4]:  # Statistics
    st.markdown("<h2 class='section-header fade-in'>Library Statistics</h2>", unsafe_allow_html=True)
    
    # Get statistics
    stats = get_stats()
    
    # Display enhanced stats cards
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
        <div class='stats-card accent'>
            <div class='stats-number'>{stats['total_authors']}</div>
            <div class='stats-label'>Unique Authors</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display genre distribution with better styling
    st.markdown("<h3 style='font-weight: 600; color: var(--primary-color); margin: 2rem 0 1rem 0; font-size: 1.25rem;'>Genre Distribution</h3>", unsafe_allow_html=True)
    if stats['genre_data']:
        # Create a simple bar chart with better styling
        genre_df = pd.DataFrame(stats['genre_data'], columns=['Genre', 'Count'])
        st.bar_chart(genre_df.set_index('Genre'))
    
    # Display year distribution with better styling
    st.markdown("<h3 style='font-weight: 600; color: var(--primary-color); margin: 2rem 0 1rem 0; font-size: 1.25rem;'>Publication Years</h3>", unsafe_allow_html=True)
    if stats['year_data']:
        # Create a simple line chart with better styling
        year_df = pd.DataFrame(stats['year_data'], columns=['Year', 'Count'])
        year_df['Year'] = year_df['Year'].astype(str)
        st.line_chart(year_df.set_index('Year'))

# Enhanced footer
st.markdown("""
<div class='footer'>
    <div class='footer-brand'>BookVerse Library System</div>
    <p>Elegantly organize your personal book collection</p>
</div>
""", unsafe_allow_html=True)  