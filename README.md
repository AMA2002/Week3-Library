# Community Library Management System

A simple console-based library management system that allows users to reserve books, cancel reservations, and view available books.

## Features

- Reserve books using email identification
- Cancel existing reservations
- View all books and their availability status
- Data persistence using text file storage
- Email validation
- User-friendly console interface

## Requirements

- Python 3.6 or higher

## File Structure

- `library_management.py`: Main program file
- `books.txt`: Database file storing book information
- `README.md`: This documentation file

## How to Run

1. Make sure you have Python installed
2. Navigate to the project directory
3. Run the program:
   ```bash
   python library_management.py
   ```

## Usage

The system provides a menu-driven interface with the following options:

1. Reserve a Book
2. Cancel Reservation
3. View All Books
Q. Quit

### Book Format in books.txt

Each book entry follows this format:
```
ID "Title" "Author" Genre Status [Email]
```

Example:
```
101 "The Great Gatsby" "F. Scott Fitzgerald" Fiction Available
102 "1984" "George Orwell" Fiction reserved user@example.com
```

## Notes

- Email validation is performed for all reservation operations
- The system automatically saves changes to the books.txt file
- Books can only be reserved if they are currently available 