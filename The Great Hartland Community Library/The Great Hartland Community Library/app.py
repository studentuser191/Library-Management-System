from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Login check decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('You need to log in first!', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Linked List implementation for books
class LinkedListNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = LinkedListNode(data)
        if not self.head:
            self.head = new_node
        else:
            last_node = self.head
            while last_node.next:
                last_node = last_node.next
            last_node.next = new_node

    def get_all_books(self):
        books = []
        current = self.head
        while current:
            books.append(current.data)
            current = current.next
        return books

    def find_by_id(self, book_id):
        current = self.head
        while current:
            if current.data['id'] == book_id:
                return current.data
            current = current.next
        return None


# HashMap implementation for book lookups (by ID and ISBN)
class BookHashMap:
    def __init__(self):
        self.books_by_id = {}  # Key: book_id, Value: book data
        self.books_by_isbn = {}  # Key: ISBN, Value: book data

    def add_book(self, book):
        self.books_by_id[book['id']] = book
        self.books_by_isbn[book['isbn']] = book

    def get_book_by_id(self, book_id):
        return self.books_by_id.get(book_id)

    def get_book_by_isbn(self, isbn):
        return self.books_by_isbn.get(isbn)


# Initialize data structures
books_linked_list = LinkedList()
books_hashmap = BookHashMap()

# In-memory checkout records
checkouts = [
    {'id': 1, 'book_id': 1, 'user_name': 'John Doe', 'checkout_date': '2024-11-01', 'checkin_date': '2024-11-15', 'returned_date': None},
    {'id': 2, 'book_id': 2, 'user_name': 'Jane Smith', 'checkout_date': '2024-10-20', 'checkin_date': '2024-11-10', 'returned_date': None},
    {'id': 3, 'book_id': 3, 'user_name': 'Emily Johnson', 'checkout_date': '2024-11-05', 'checkin_date': '2024-11-19', 'returned_date': '2024-11-17'},
    {'id': 4, 'book_id': 4, 'user_name': 'Michael Brown', 'checkout_date': '2024-11-10', 'checkin_date': '2024-11-24', 'returned_date': None},
    {'id': 5, 'book_id': 5, 'user_name': 'Sarah Williams', 'checkout_date': '2024-10-25', 'checkin_date': '2024-11-05', 'returned_date': '2024-11-03'},
    {'id': 6, 'book_id': 6, 'user_name': 'David Taylor', 'checkout_date': '2024-11-01', 'checkin_date': '2024-11-15', 'returned_date': None},
    {'id': 7, 'book_id': 7, 'user_name': 'Sophia Martinez', 'checkout_date': '2024-11-02', 'checkin_date': '2024-11-16', 'returned_date': None},
    {'id': 8, 'book_id': 8, 'user_name': 'James Wilson', 'checkout_date': '2024-10-30', 'checkin_date': '2024-11-13', 'returned_date': '2024-11-12'},
    {'id': 9, 'book_id': 9, 'user_name': 'Olivia Anderson', 'checkout_date': '2024-11-03', 'checkin_date': '2024-11-17', 'returned_date': None},
    {'id': 10, 'book_id': 10, 'user_name': 'Daniel Lee', 'checkout_date': '2024-10-28', 'checkin_date': '2024-11-12', 'returned_date': '2024-11-10'}
]


# Initialize books (and populate both Linked List and HashMap)
initial_books = [
    {'id': 1, 'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'year': 1925, 'isbn': '9780743273565', 'status': 'available'},
    {'id': 2, 'title': '1984', 'author': 'George Orwell', 'year': 1949, 'isbn': '9780451524935', 'status': 'available'},
    {'id': 3, 'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'year': 1960, 'isbn': '9780061120084', 'status': 'available'},
    {'id': 4, 'title': 'Pride and Prejudice', 'author': 'Jane Austen', 'year': 1813, 'isbn': '9781503290563', 'status': 'available'},
    {'id': 5, 'title': 'The Catcher in the Rye', 'author': 'J.D. Salinger', 'year': 1951, 'isbn': '9780316769488', 'status': 'available'},
    {'id': 6, 'title': 'The Hobbit', 'author': 'J.R.R. Tolkien', 'year': 1937, 'isbn': '9780618968633', 'status': 'available'},
    {'id': 7, 'title': 'Moby Dick', 'author': 'Herman Melville', 'year': 1851, 'isbn': '9781503280786', 'status': 'available'},
    {'id': 8, 'title': 'War and Peace', 'author': 'Leo Tolstoy', 'year': 1869, 'isbn': '9781853260629', 'status': 'available'},
    {'id': 9, 'title': 'The Da Vinci Code', 'author': 'Dan Brown', 'year': 2003, 'isbn': '9780307474278', 'status': 'available'},
    {'id': 10, 'title': 'The Hunger Games', 'author': 'Suzanne Collins', 'year': 2008, 'isbn': '9780439023481', 'status': 'available'}
]

for book in initial_books:
    books_linked_list.append(book)
    books_hashmap.add_book(book)


# Home page
@app.route('/')
@login_required
def index():
    return render_template('index.html')


# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Checking if the username and password match
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password!', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')


# Logout page
@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))  # Redirecting to login page after logging out



# Add book
@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        isbn = request.form['isbn']

        # Validation
        if not title or not author or not year or not isbn:
            flash('All fields are required!', 'error')
            return redirect(url_for('add_book'))

        if not year.isdigit():
            flash('Year must be a number!', 'error')
            return redirect(url_for('add_book'))

        # Checking for duplicate ISBN using the HashMap
        if books_hashmap.get_book_by_isbn(isbn):
            flash('A book with this ISBN already exists!', 'error')
            return redirect(url_for('add_book'))

        # Adding the book to both LinkedList and HashMap
        book_id = len(books_linked_list.get_all_books()) + 1
        new_book = {
            'id': book_id,
            'title': title,
            'author': author,
            'year': int(year),
            'isbn': isbn,
            'status': 'available'
        }

        books_linked_list.append(new_book)
        books_hashmap.add_book(new_book)

        flash('Book added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add_book.html')


# List books
@app.route('/list')
def list_books():
    books = books_linked_list.get_all_books()  # Getting books from the LinkedList
    return render_template('list_books.html', books=books)


# Change book status
@app.route('/change_book_status/<int:book_id>/<status>', methods=['POST'])
def change_book_status(book_id, status):
    book = books_hashmap.get_book_by_id(book_id)
    if book:
        book['status'] = status
        flash(f'Book status updated to {status}.', 'success')
    return redirect(url_for('list_books'))


# Search books
@app.route('/search', methods=['GET', 'POST'])
def search_book():
    if request.method == 'POST':
        query = request.form['query']

        if not query:
            flash('Search query cannot be empty!', 'error')
            return redirect(url_for('search_book'))

        # Search by title or author
        results = [book for book in books_linked_list.get_all_books() if
                   query.lower() in book['title'].lower() or query.lower() in book['author'].lower()]
        return render_template('search_book.html', books=results, query=query)

    return render_template('search_book.html', books=None)


# Checkout book
@app.route('/checkout_book', methods=['GET', 'POST'])
def checkout_book():
    if request.method == 'POST':
        book_id = int(request.form['book_id'])
        user_name = request.form['user_name']
        checkout_date = request.form['checkout_date']
        checkin_date = request.form['checkin_date']

        # Find the book and update its status
        book = books_hashmap.get_book_by_id(book_id)
        if book and book['status'] == 'available':
            book['status'] = 'checked out'
            checkouts.append({
                'id': len(checkouts) + 1,
                'book_id': book_id,
                'user_name': user_name,
                'checkout_date': checkout_date,
                'checkin_date': checkin_date,
                'returned_date': None
            })
            flash('Book checked out successfully!', 'success')
            return redirect(url_for('list_books'))

        flash('The book is not available for checkout.', 'error')
        return redirect(url_for('checkout_book'))

    # Get the list of available books for checkout
    available_books = [book for book in books_linked_list.get_all_books() if book['status'] == 'available']
    return render_template('checkout_book.html', books=available_books)


# Check-in book
@app.route('/checkin_book/<int:checkout_id>', methods=['POST'])
def checkin_book(checkout_id):
    for checkout in checkouts:
        if checkout['id'] == checkout_id and not checkout['returned_date']:
            # Update the returned date
            checkout['returned_date'] = datetime.now().strftime('%Y-%m-%d')

            # Update the book status
            book = books_hashmap.get_book_by_id(checkout['book_id'])
            if book:
                book['status'] = 'available'

            flash('Book checked in successfully!', 'success')
            break
    return redirect(url_for('list_books'))


@app.route('/checked_out')
def checked_out_books():
    checked_out_details = [
        {
            'id': checkout_id,
            'book_title': next(
                (book['title'] for book in books_linked_list.get_all_books() if book['id'] == checkout['book_id']),
                'Unknown Book'),
            'user_name': checkout['user_name'],
            'checkout_date': checkout['checkout_date'],
            'expected_checkin_date': checkout['checkin_date'],
            'actual_checkin_date': checkout['returned_date'] if checkout['returned_date'] else 'Not Returned Yet'
        }
        for checkout_id, checkout in enumerate(checkouts, start=1)
    ]
    return render_template('checked_out_books.html', checkouts=checked_out_details)


if __name__ == '__main__':
    app.run(debug=True)
