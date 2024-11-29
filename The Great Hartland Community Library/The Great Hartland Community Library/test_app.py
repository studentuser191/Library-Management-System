import unittest
from flask import Flask
from app import app, books_hashmap, checkouts


class BookAdditionTests(unittest.TestCase):

    def setUp(self):
        """Set up the test client"""
        self.app = app.test_client()
        self.app.secret_key = 'supersecretkey'

    def login(self):
        """Helper function to log in as admin"""
        return self.app.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        })

    def test_add_book_success(self):
        """Test the successful addition of a book"""
        # First, log in
        self.login()

        # Now add the book
        response = self.app.post('/add', data={
            'title': 'New Book',
            'author': 'John Doe',
            'year': '2024',
            'isbn': '1234567890123'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Book added successfully!', response.data)

        # Check if user is logged in (session should contain 'logged_in')
        with self.app.session_transaction() as session:
            self.assertTrue('logged_in' in session)  # Check login status

    def test_add_book_missing_fields(self):
        """Test the addition of a book with missing fields"""
        # First, log in
        self.login()

        # Now attempt to add the book with missing fields
        response = self.app.post('/add', data={
            'title': 'Incomplete Book',
            'author': '',  # Missing author
            'year': '2024',
            'isbn': '1234567890123'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All fields are required!', response.data)

    def test_add_book_invalid_year(self):
        """Test the addition of a book with an invalid year format"""
        # First, log in
        self.login()

        # Attempt to add a book with an invalid year
        response = self.app.post('/add', data={
            'title': 'Invalid Year Book',
            'author': 'Author C',
            'year': 'Year2024',  # Invalid year (non-numeric)
            'isbn': '1234567890124'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)  # Check if the redirected page loads
        self.assertIn(b'Year must be a number!', response.data)  # Flash error message for invalid year


class BookCheckoutTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the test client"""
        cls.client = app.test_client()
        cls.client.get('/login', follow_redirects=True)  # Simulate login
        # Ensure the books are reset to initial state
        checkouts.clear()



    def test_checkout_unavailable_book(self):
        """Test the attempt to checkout an unavailable book"""
        book_id = 1  # Assuming this book is now checked out
        user_name = 'Bob'
        checkout_date = '2024-11-26'
        checkin_date = '2024-12-03'

        # First, checkout the book
        self.client.post('/checkout_book', data={
            'book_id': book_id,
            'user_name': user_name,
            'checkout_date': checkout_date,
            'checkin_date': checkin_date
        }, follow_redirects=True)

        # Attempt to checkout the same book again (book 1)
        response = self.client.post('/checkout_book', data={
            'book_id': book_id,
            'user_name': 'Charlie',
            'checkout_date': '2024-11-27',
            'checkin_date': '2024-12-04'
        }, follow_redirects=True)

        # Assert that the second checkout attempt fails
        self.assertIn(b'The book is not available for checkout.', response.data)






if __name__ == '__main__':
    unittest.main()
