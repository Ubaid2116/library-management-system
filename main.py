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

# Custom CSS with enhanced UI, bolder text, and more attractive styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&family=Playfair+Display:wght@500;600;700;800;900&display=swap');
    
    :root {
        --primary-color: #6366F1;
        --secondary-color: #EC4899;
        --accent-color: #10B981;
        --background-color: #F8FAFC;
        --card-color: #FFFFFF;
        --text-primary: #1E293B;
        --text-secondary: #475569;
        --text-tertiary: #94A3B8;
        --shadow: rgba(99, 102, 241, 0.15);
        --gradient-primary: linear-gradient(135deg, #6366F1, #8B5CF6);
        --gradient-secondary: linear-gradient(135deg, #EC4899, #F43F5E);
        --filter-bg: #EEF2FF;
        --filter-border: #C7D2FE;
        --filter-shadow: rgba(99, 102, 241, 0.1);
    }
    
    .dark {
        --primary-color: #818CF8;
        --secondary-color: #F472B6;
        --accent-color: #34D399;
        --background-color: #0F172A;
        --card-color: #1E293B;
        --text-primary: #F1F5F9;
        --text-secondary: #CBD5E1;
        --text-tertiary: #94A3B8;
        --shadow: rgba(0, 0, 0, 0.3);
        --filter-bg: #1E293B;
        --filter-border: #4B5563;
        --filter-shadow: rgba(0, 0, 0, 0.2);
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: var(--background-color);
        font-family: 'Montserrat', sans-serif;
        color: var(--text-primary);
        transition: all 0.3s ease;
    }
    
    /* Main header styling - BOLDER */
    .main-header {
        font-family: 'Playfair Display', serif;
        font-size: 4rem;
        font-weight: 900;
        -webkit-background-clip: text;
        text-align: center;
        margin: 2rem 0;
        padding-bottom: 0.5rem;
        letter-spacing: -0.5px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Sub header styling - BOLDER */
    .sub-header {
        font-family: 'Playfair Display', serif;
        font-size: 2.5rem;
        font-weight: 800;
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
        width: 80px;
        height: 5px;
        background: var(--gradient-secondary);
        border-radius: 3px;
    }
    
    /* Card styling with enhanced hover effects */
    .book-card {
        background-color: var(--card-color);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px var(--shadow);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border-top: 6px solid var(--primary-color);
        position: relative;
        overflow: hidden;
    }
    
    .book-card:hover {
        transform: translateY(-12px) scale(1.02);
        box-shadow: 0 20px 40px var(--shadow);
    }
    
    .book-card::before {
        content: "";
        position: absolute;
        top: 0;
        right: 0;
        width: 0;
        height: 0;
        border-style: solid;
        border-width: 0 70px 70px 0;
        border-color: transparent var(--primary-color) transparent transparent;
        opacity: 0.2;
    }
    
    /* Book title styling - BOLDER */
    .book-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        font-weight: 800;
        color: var(--primary-color);
        margin-bottom: 0.8rem;
        line-height: 1.3;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    /* Book author styling - BOLDER */
    .book-author {
        font-size: 1.2rem;
        font-weight: 700;
        color: var(--secondary-color);
        margin-bottom: 1.2rem;
        font-style: italic;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    /* Book details styling - BOLDER */
    .book-details {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-secondary);
        margin-bottom: 0.8rem;
        display: flex;
        align-items: flex-start;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    .book-details i {
        margin-right: 0.8rem;
        color: var(--accent-color);
        font-size: 1.2rem;
        flex-shrink: 0;
    }
    
    /* Badge styling - ENHANCED */
    .badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 30px;
        font-size: 0.9rem;
        font-weight: 700;
        margin-right: 0.7rem;
        margin-bottom: 0.7rem;
        background: var(--gradient-primary);
        color: white;
        box-shadow: 0 4px 8px rgba(99, 102, 241, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        word-wrap: break-word;
        overflow-wrap: break-word;
        max-width: 100%;
    }
    
    .badge-fiction {
        background: linear-gradient(135deg, #6366F1, #818CF8);
    }
    
    .badge-nonfiction {
        background: linear-gradient(135deg, #10B981, #34D399);
    }
    
    .badge-scifi {
        background: linear-gradient(135deg, #EC4899, #F472B6);
    }
    
    .badge-fantasy {
        background: linear-gradient(135deg, #F59E0B, #FBBF24);
    }
    
    .badge-mystery {
        background: linear-gradient(135deg, #8B5CF6, #A78BFA);
    }
    
    .badge-thriller {
        background: linear-gradient(135deg, #EF4444, #F87171);
    }
    
    .badge-romance {
        background: linear-gradient(135deg, #EC4899, #F9A8D4);
    }
    
    .badge-biography {
        background: linear-gradient(135deg, #10B981, #6EE7B7);
    }
    
    .badge-history {
        background: linear-gradient(135deg, #3B82F6, #93C5FD);
    }
    
    .badge-selfhelp {
        background: linear-gradient(135deg, #8B5CF6, #C4B5FD);
    }
    
    .badge-other {
        background: linear-gradient(135deg, #6B7280, #9CA3AF);
    }
    
    /* Button styling - ENHANCED */
    .stButton button {
        background: var(--gradient-primary);
        color: white;
        font-weight: 700;
        border-radius: 12px;
        padding: 0.8rem 1.5rem;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 6px 15px rgba(99, 102, 241, 0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
        width: 100%;
        white-space: normal;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    .stButton button:hover {
        background: var(--gradient-secondary);
        box-shadow: 0 8px 20px rgba(236, 72, 153, 0.4);
        transform: translateY(-3px);
    }
    
    /* Delete button styling */
    .delete-btn {
        background: linear-gradient(135deg, #EF4444, #F87171) !important;
        box-shadow: 0 6px 15px rgba(239, 68, 68, 0.3) !important;
    }
    
    .delete-btn:hover {
        background: linear-gradient(135deg, #DC2626, #EF4444) !important;
        box-shadow: 0 8px 20px rgba(220, 38, 38, 0.4) !important;
    }
    
    /* Form styling - ENHANCED */
    .stTextInput input, .stTextArea textarea, .stNumberInput div[data-baseweb="input"] input {
        background-color: var(--card-color);
        border: 2px solid #E2E8F0;
        border-radius: 12px;
        padding: 0.8rem 1.2rem;
        font-family: 'Montserrat', sans-serif;
        font-weight: 500;
        color: var(--text-primary);
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        width: 100%;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    /* NEW FILTER STYLING */
    .stSelectbox div[data-baseweb="select"] {
        background-color: var(--filter-bg) !important;
        border: 2px solid var(--filter-border) !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 12px var(--filter-shadow) !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox div[data-baseweb="select"]:hover {
        border-color: var(--primary-color) !important;
        box-shadow: 0 6px 16px var(--filter-shadow) !important;
        transform: translateY(-2px) !important;
    }
    
    .stSelectbox div[data-baseweb="select"] div {
        background-color: transparent !important;
        font-weight: 600 !important;
        color: var(--primary-color) !important;
        padding: 0.7rem 1rem !important;
    }
    
    .stSelectbox label {
        background-color: var(--card-color) !important;
        color: var(--primary-color) !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 0.3rem 0.8rem !important;
        border-radius: 8px !important;
        margin-bottom: 0.5rem !important;
        display: inline-block !important;
        box-shadow: 0 2px 5px var(--filter-shadow) !important;
    }
    
    /* Filter container styling */
    .filter-container {
        background-color: var(--card-color);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 20px var(--shadow);
        border-left: 5px solid var(--primary-color);
    }
    
    .filter-title {
        font-weight: 800;
        color: var(--primary-color);
        font-size: 1.2rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
    }
    
    .filter-title svg {
        margin-right: 0.5rem;
    }
    
    /* Fix for select boxes */
    .stSelectbox div[data-baseweb="select"] div[data-testid="stMarkdownContainer"] p {
        white-space: normal !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }
    
    /* Fix for labels */
    .stTextInput label, .stTextArea label, .stSelectbox label, .stNumberInput label {
        font-weight: 600;
        color: var(--text-primary);
        font-size: 1rem;
        word-wrap: break-word;
        overflow-wrap: break-word;
        white-space: normal;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox div[data-baseweb="select"] div:focus, .stNumberInput div[data-baseweb="input"] input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: 700;
        color: var(--primary-color);
        background-color: var(--card-color);
        border-radius: 12px;
        padding: 0.8rem 1.2rem;
        word-wrap: break-word;
        overflow-wrap: break-word;
        white-space: normal;
    }
    
    /* Sidebar styling - ENHANCED */
    [data-testid="stSidebar"] {
        background-color: var(--card-color);
        border-right: none;
        box-shadow: 5px 0 20px var(--shadow);
    }
    
    .sidebar-content {
        padding: 2.5rem 1.5rem;
    }
    
    .sidebar-title {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        font-weight: 800;
        color: var(--primary-color);
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .sidebar-subtitle {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--secondary-color);
        margin: 1.8rem 0 1.2rem 0;
    }
    
    /* Animation classes - ENHANCED */
    .fade-in {
        animation: fadeIn 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Stats card styling - ENHANCED */
    .stats-card {
        background: var(--gradient-primary);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 15px 30px var(--shadow);
        text-align: center;
        transition: all 0.4s ease;
        color: white;
    }
    
    .stats-card:hover {
        transform: translateY(-8px) scale(1.03);
        box-shadow: 0 20px 40px var(--shadow);
    }
    
    .stats-number {
        font-size: 3.5rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.8rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .stats-label {
        font-size: 1.2rem;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.9);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Search box styling - ENHANCED */
    .search-container {
        background-color: var(--filter-bg);
        border-radius: 50px;
        padding: 0.5rem;
        box-shadow: 0 8px 20px var(--filter-shadow);
        margin-bottom: 2.5rem;
        border: 2px solid var(--filter-border);
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
    }
    
    .search-container:hover, .search-container:focus-within {
        box-shadow: 0 12px 25px var(--filter-shadow);
        transform: translateY(-3px);
        border-color: var(--primary-color);
    }
    
    .search-icon {
        margin-left: 1rem;
        color: var(--primary-color);
        font-size: 1.5rem;
    }
    
    .search-input {
        flex: 1;
        background: transparent;
        border: none;
        padding: 1rem;
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-primary);
    }
    
    .search-input:focus {
        outline: none;
    }
    
    /* Custom search input styling */
    .stTextInput[data-testid="stTextInput"] > div:first-child {
        background-color: var(--filter-bg) !important;
        border-radius: 50px !important;
        border: 2px solid var(--filter-border) !important;
        box-shadow: 0 8px 20px var(--filter-shadow) !important;
        transition: all 0.3s ease !important;
        padding: 0.3rem !important;
    }
    
    .stTextInput[data-testid="stTextInput"] > div:first-child:hover {
        border-color: var(--primary-color) !important;
        box-shadow: 0 12px 25px var(--filter-shadow) !important;
        transform: translateY(-3px) !important;
    }
    
    .stTextInput[data-testid="stTextInput"] input {
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
        font-weight: 600 !important;
        color: var(--primary-color) !important;
    }
    
    /* Empty state styling - ENHANCED */
    .empty-state {
        text-align: center;
        padding: 4rem 0;
        background-color: var(--card-color);
        border-radius: 20px;
        box-shadow: 0 10px 25px var(--shadow);
        margin: 2rem 0;
    }
    
    .empty-state-icon {
        font-size: 6rem;
        color: var(--primary-color);
        margin-bottom: 2rem;
        opacity: 0.8;
    }
    
    .empty-state-text {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-secondary);
        margin-bottom: 2rem;
    }
    
    /* Footer styling - ENHANCED */
    .footer {
        text-align: center;
        padding: 3rem 0;
        color: var(--text-tertiary);
        font-size: 1rem;
        font-weight: 500;
        background-color: var(--card-color);
        border-radius: 20px 20px 0 0;
        margin-top: 3rem;
        box-shadow: 0 -5px 20px rgba(0, 0, 0, 0.05);
    }
    
    .footer a {
        color: var(--primary-color);
        text-decoration: none;
        font-weight: 700;
    }
    
    /* Book cover styling - ENHANCED */
    .book-cover {
        width: 100%;
        height: 250px;
        background: var(--gradient-primary);
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-family: 'Playfair Display', serif;
        font-weight: 800;
        font-size: 1.5rem;
        text-align: center;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    .book-cover::after {
        content: "📖";
        position: absolute;
        bottom: 10px;
        right: 10px;
        font-size: 2rem;
        opacity: 0.5;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: var(--card-color);
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        font-weight: 700;
        white-space: normal;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--primary-color);
        color: white;
    }
    
    /* Chart styling */
    [data-testid="stVegaLiteChart"] {
        background-color: var(--card-color);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 10px 25px var(--shadow);
    }
    
    /* Fix for filter and sort dropdowns */
    .stSelectbox[data-testid="stSelectbox"] {
        margin-bottom: 20px;
    }
    
    /* Fix for text overflow in all elements */
    [data-testid="stVerticalBlock"] > div {
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        white-space: normal !important;
    }
    
    /* Fix for description text */
    .streamlit-expanderContent p {
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        white-space: normal !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
        color: var(--text-secondary) !important;
    }
    
    /* Fix for success/error messages */
    .stAlert {
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        white-space: normal !important;
    }
    
    .stAlert p {
        font-weight: 600 !important;
        font-size: 1rem !important;
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
def get_random_gradient():
    gradients = [
        "linear-gradient(135deg, #6366F1, #8B5CF6)",
        "linear-gradient(135deg, #EC4899, #F43F5E)",
        "linear-gradient(135deg, #10B981, #34D399)",
        "linear-gradient(135deg, #F59E0B, #FBBF24)",
        "linear-gradient(135deg, #3B82F6, #60A5FA)",
        "linear-gradient(135deg, #8B5CF6, #A78BFA)",
        "linear-gradient(135deg, #EC4899, #F9A8D4)",
        "linear-gradient(135deg, #EF4444, #F87171)"
    ]
    return random.choice(gradients)

# Main content
st.markdown("<h1 class='main-header'>📚 BookVerse</h1>", unsafe_allow_html=True)

# Create tabs with better styling
tabs = st.tabs(["📚 Browse", "➕ Add Book", "✏️ Edit Books", "🔍 Search", "📊 Statistics"])

with tabs[0]:  # Browse Books
    st.markdown("<h2 class='sub-header fade-in'>📖 Book Collection</h2>", unsafe_allow_html=True)
    
    books = get_all_books()
    
    # Filter options with completely redesigned styling
    st.markdown("""
    <div class="filter-container fade-in">
        <div class="filter-title">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon>
            </svg>
            Filter & Sort Books
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
                gradient = get_random_gradient()
                st.markdown(f"""
                <div class='book-card fade-in'>
                    <div class='book-cover' style='background: {gradient};'>
                        {book['title']}
                    </div>
                    <div class='book-title'>{book['title']}</div>
                    <div class='book-author'>by {book['author']}</div>
                    <div class='book-details'><i>📅</i> Published: {book['year']}</div>
                    <div class='book-details'><i>📖</i> Genre: {book['genre']}</div>
                    <div class='badge badge-{book["genre"].lower().replace(" ", "")}'>{book['genre']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("📝 Description"):
                    st.write(book['description'])
    else:
        st.info("No books found matching your criteria.")

with tabs[1]:  # Add Book
    st.markdown("<h2 class='sub-header fade-in'>➕ Add New Book</h2>", unsafe_allow_html=True)
    
    # Enhanced form with better styling
    with st.form("add_book_form"):
        title = st.text_input("📕 Title", max_chars=100)
        author = st.text_input("✍️ Author", max_chars=100)
        genre = st.selectbox("🏷️ Genre", ["Fiction", "Non-Fiction", "Science Fiction", "Fantasy", 
                                      "Mystery", "Thriller", "Romance", "Biography", 
                                      "History", "Self-Help", "Magical Realism", "Coming-of-age",
                                      "Psychological Fiction", "Other"])
        year = st.number_input("📅 Publication Year", min_value=1000, max_value=datetime.now().year, 
                              value=2020, step=1)
        isbn = st.text_input("🔢 ISBN", max_chars=20)
        description = st.text_area("📝 Description", height=150)
        
        submitted = st.form_submit_button("Add Book to Library")
        
        if submitted:
            if title and author:
                add_book(title, author, genre, year, isbn, description)
                st.success(f"Book '{title}' has been added successfully!")
                st.balloons()
                
                # Show success card with enhanced styling
                gradient = get_random_gradient()
                st.markdown(f"""
                <div class='book-card fade-in'>
                    <div class='book-cover' style='background: {gradient};'>
                        {title}
                    </div>
                    <div class='book-title'>{title}</div>
                    <div class='book-author'>by {author}</div>
                    <div class='book-details'><i>📅</i> Published: {year}</div>
                    <div class='book-details'><i>📖</i> Genre: {genre}</div>
                    <div class='badge badge-{genre.lower().replace(" ", "")}'>{genre}</div>
                    <p style="font-weight: 700; color: var(--accent-color); margin-top: 15px; font-size: 1.1rem;">✅ Book added to your library!</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Title and Author are required fields.")

with tabs[2]:  # Edit Books
    st.markdown("<h2 class='sub-header fade-in'>✏️ Edit or Delete Books</h2>", unsafe_allow_html=True)
    
    books = get_all_books()
    if not books.empty:
        # Create a searchable dropdown with redesigned styling
        st.markdown("""
        <div class="filter-container fade-in">
            <div class="filter-title">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
        
        # Display book details in an enhanced card
        gradient = get_random_gradient()
        st.markdown(f"""
        <div class='book-card fade-in'>
            <div class='book-cover' style='background: {gradient};'>
                {selected_book['title']}
            </div>
            <div class='book-title'>{selected_book['title']}</div>
            <div class='book-author'>by {selected_book['author']}</div>
            <div class='book-details'><i>📅</i> Published: {selected_book['year']}</div>
            <div class='book-details'><i>📖</i> Genre: {selected_book['genre']}</div>
            <div class='badge badge-{selected_book["genre"].lower().replace(" ", "")}'>{selected_book['genre']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced form with better styling
        with st.form("edit_book_form"):
            st.markdown("<p style='font-weight: 700; font-size: 1.2rem; margin-bottom: 15px; color: var(--primary-color);'>📝 Edit Book Details</p>", unsafe_allow_html=True)
            edit_title = st.text_input("📕 Title", value=selected_book['title'], max_chars=100)
            edit_author = st.text_input("✍️ Author", value=selected_book['author'], max_chars=100)
            edit_genre = st.selectbox("🏷️ Genre", ["Fiction", "Non-Fiction", "Science Fiction", "Fantasy", 
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
            edit_year = st.number_input("📅 Publication Year", min_value=1000, max_value=datetime.now().year, 
                                       value=int(selected_book['year']), step=1)
            edit_isbn = st.text_input("🔢 ISBN", value=selected_book['isbn'] if selected_book['isbn'] else "", max_chars=20)
            edit_description = st.text_area("📝 Description", value=selected_book['description'] if selected_book['description'] else "", height=150)
            
            col1_btn, col2_btn = st.columns(2)
            with col1_btn:
                update_button = st.form_submit_button("💾 Update Book")
            with col2_btn:
                delete_button = st.form_submit_button("🗑️ Delete Book", type="primary", help="This action cannot be undone")
            
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
                st.rerun()  # Using st.rerun() instead of st.experimental_rerun()
    else:
        # Enhanced empty state
        st.markdown("""
        <div class='empty-state'>
            <div class='empty-state-icon'>📚</div>
            <div class='empty-state-text'>No books in your library yet.</div>
            <p style="font-weight: 600; font-size: 1.1rem; color: var(--text-secondary);">Add some books to get started!</p>
        </div>
        """, unsafe_allow_html=True)

with tabs[3]:  # Search
    st.markdown("<h2 class='sub-header fade-in'>🔍 Search Books</h2>", unsafe_allow_html=True)
    
    # Enhanced search box with completely redesigned styling
    st.markdown("""
    <div class="filter-container fade-in">
        <div class="filter-title">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
            Find Books in Your Library
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
                    gradient = get_random_gradient()
                    st.markdown(f"""
                    <div class='book-card fade-in'>
                        <div class='book-cover' style='background: {gradient};'>
                            {book['title']}
                        </div>
                        <div class='book-title'>{book['title']}</div>
                        <div class='book-author'>by {book['author']}</div>
                        <div class='book-details'><i>📅</i> Published: {book['year']}</div>
                        <div class='book-details'><i>📖</i> Genre: {book['genre']}</div>
                        <div class='badge badge-{book["genre"].lower().replace(" ", "")}'>{book['genre']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander("📝 Description"):
                        st.write(book['description'])
        else:
            # Enhanced empty search results
            st.markdown("""
            <div class='empty-state'>
                <div class='empty-state-icon'>🔍</div>
                <div class='empty-state-text'>No books found matching your search.</div>
                <p style="font-weight: 600; font-size: 1.1rem; color: var(--text-secondary);">Try a different search term or browse all books.</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        # Enhanced search tips
        st.markdown("""
        <div style="background-color: var(--card-color); border-radius: 20px; padding: 25px; box-shadow: 0 10px 25px var(--shadow); margin-top: 20px;">
            <h3 style="font-weight: 800; color: var(--primary-color); margin-bottom: 20px; font-size: 1.5rem;">🔍 Search Tips</h3>
            <ul style="font-weight: 600; font-size: 1.1rem; color: var(--text-secondary); margin-left: 20px; line-height: 2;">
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
        <div class='stats-card' style="background: linear-gradient(135deg, #EC4899, #F43F5E);">
            <div class='stats-number'>{stats['total_authors']}</div>
            <div class='stats-label'>Unique Authors</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display genre distribution with better styling
    st.markdown("<h3 style='font-weight: 800; color: var(--primary-color); margin: 30px 0 20px 0; font-size: 1.8rem;'>📊 Genre Distribution</h3>", unsafe_allow_html=True)
    if stats['genre_data']:
        # Create a simple bar chart with better styling
        genre_df = pd.DataFrame(stats['genre_data'], columns=['Genre', 'Count'])
        st.bar_chart(genre_df.set_index('Genre'))
    
    # Display year distribution with better styling
    st.markdown("<h3 style='font-weight: 800; color: var(--primary-color); margin: 30px 0 20px 0; font-size: 1.8rem;'>📈 Publication Years</h3>", unsafe_allow_html=True)
    if stats['year_data']:
        # Create a simple line chart with better styling
        year_df = pd.DataFrame(stats['year_data'], columns=['Year', 'Count'])
        year_df['Year'] = year_df['Year'].astype(str)
        st.line_chart(year_df.set_index('Year'))

# Enhanced footer
st.markdown("---")
st.markdown("""
<div class='footer'>
    <p style="font-weight: 700; font-size: 1.3rem; color: var(--primary-color); margin-bottom: 10px;">📚 BookVerse | Modern Library Management System</p>
    <p style="font-weight: 600; font-size: 1rem;">Created with ❤️ using Streamlit and SQLite</p>
</div>
""", unsafe_allow_html=True)