# Import required libraries
from flask import Flask , render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database configuration
DB_NAME = 'library.db'

# Create a database connection
def create_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn

# Initialize the database
def initialize_database():
    conn = create_connection()
    c = conn.cursor()
    
    # Create books table
    c.execute('''CREATE TABLE IF NOT EXISTS books
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT NOT NULL,
                 author TEXT NOT NULL,
                 stock INTEGER NOT NULL)''')
    
    # Create members table
    c.execute('''CREATE TABLE IF NOT EXISTS members
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 debt INTEGER NOT NULL)''')
    
    # Create transactions table
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 book_id INTEGER NOT NULL,
                 member_id INTEGER NOT NULL,
                 issue_date DATE NOT NULL,
                 return_date DATE,
                 FOREIGN KEY (book_id) REFERENCES books (id),
                 FOREIGN KEY (member_id) REFERENCES members (id))''')
    
    # Save the changes
    conn.commit()
    conn.close()

# Initialize the database
initialize_database()

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Books page
@app.route('/books')
def books():
    conn = create_connection()
    c = conn.cursor()
    
    # Retrieve all books from the database
    c.execute('SELECT * FROM books')
    books = c.fetchall()
    
    # Close the connection
    conn.close()
    
    return render_template('books.html', books=books)

# Add a book
@app.route('/books/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        stock = int(request.form['stock'])
        
        conn = create_connection()
        c = conn.cursor()
        
        # Insert the new book into the database
        c.execute('INSERT INTO books (title, author, stock) VALUES (?, ?, ?)', (title, author, stock))
        
        # Save the changes
        conn.commit()
        conn.close()
        
        return redirect(url_for('books'))
    
    return render_template('add_book.html')

# Members page
@app.route('/members')
def members():
    conn = create_connection()
    c = conn.cursor()
    
    # Retrieve all members from the database
    c.execute('SELECT * FROM members')
    members = c.fetchall()
    
    # Close the connection
    conn.close()
    
    return render_template('members.html', members=members)

# Add a member
@app.route('/members/add', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        name = request.form['name']
        
        conn = create_connection()
        c = conn.cursor()
        
        # Insert the new member into the database
        c.execute('INSERT INTO members (name, debt) VALUES (?, ?)', (name, 0))
        
        # Save the changes
        conn.commit()
        conn.close()
        
        return redirect(url_for('members'))
    
    return render_template('add_member.html')

# Issue a book to a member
@app.route('/issue_book', methods=['POST'])
def issue_book():
    member_id = int(request.form['member_id'])
    book_id = int(request.form['book_id'])
    
    conn = create_connection()
    c = conn.cursor()
    
    # Retrieve the selected book from the database
    c.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    book = c.fetchone()
    
    # Retrieve the selected member from the database
    c.execute('SELECT * FROM members WHERE id = ?', (member_id,))
    member = c.fetchone()
    
    # Check if the book and member exist
    if book and member:
        stock = book[3]
        debt = member[2]
        
        # Check if the book is in stock
        if stock > 0:
            # Update the stock
            stock -= 1
            
            # Update the book stock in the database
            c.execute('UPDATE books SET stock = ? WHERE id = ?', (stock, book_id))
            
            # Insert the transaction into the database
            c.execute('INSERT INTO transactions (book_id, member_id, issue_date) VALUES (?, ?, CURRENT_DATE)', (book_id, member_id))
            
            # Save the changes
            conn.commit()
    
    # Close the connection
    conn.close()
    
    #return redirect(url_for('home'))
# Calculate the rent fee for the returned book
def calculate_rent_fee(transaction):
    # Placeholder logic to calculate rent fee
    # Modify this function as per your requirements
    return 0  # Replace with your actual rent fee calculation logic
# Render the transactions page
@app.route('/transactions')
def transactions():
    conn = create_connection()
    c = conn.cursor()

    # Retrieve all transactions from the database
    c.execute('SELECT * FROM transactions')
    transactions = c.fetchall()

    # Close the connection
    conn.close()

    return render_template('transactions.html', transactions=transactions)
# Return a book from a member
@app.route('/return_book', methods=['GET','POST'])
def return_book():
    if request.method=='POST':
        member_id = int(request.form['member_id'])
        book_id = int(request.form['book_id'])
    
    conn = create_connection()
    c = conn.cursor()
    
    # Retrieve the selected book from the database
    c.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    book = c.fetchone()
    
    # Retrieve the selected member from the database
    c.execute('SELECT * FROM members WHERE id = ?', (member_id,))
    member = c.fetchone()
    
    # Check if the book and member exist
    if book and member:
        stock = book[3]
        debt = member[2]
        
        # Update the stock and debt if the book is returned by the member
        stock += 1
        rent_fee = calculate_rent_fee(debt)  # Calculate the rent fee based on the member's debt
        
        # Update the book stock and member debt in the database
        c.execute('UPDATE books SET stock = ? WHERE id = ?', (stock, book_id))
        c.execute('UPDATE members SET debt = ? WHERE id = ?', (debt + rent_fee, member_id))
        
        # Insert the return transaction into the database
        c.execute('INSERT INTO transactions (book_id, member_id, return_date, rent_fee) VALUES (?, ?, CURRENT_DATE, ?)', (book_id, member_id, rent_fee))
        
        # Save the changes
        conn.commit()
    
    # Close the connection
    conn.close()
    
    return render_template('return_book.html',book_id=book_id)
# Search for a book by name and author
@app.route('/search', methods=['POST','GET'])
def search():
    keyword=''
    if request.method=='POST':
        keyword = request.form['keyword']
    
    conn = create_connection()
    c = conn.cursor()
    
    # Search for books by title or author
    c.execute("SELECT * FROM books WHERE title LIKE '%' || ? || '%' OR author LIKE '%' || ? || '%'", (keyword, keyword))
    books = c.fetchall()
    
    # Close the connection
    conn.close()
    
    return render_template('search_results.html', books=books)

if __name__=='__main__':
    app.run(debug=True)
# Run the application