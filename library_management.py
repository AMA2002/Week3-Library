import os
import re
from typing import Dict

class Book:
    def __init__(self, id: str, title: str, author: str, genre: str, status: str = "Available", reserved_by: str = None):
        self.id = id
        self.title = title
        self.author = author
        self.genre = genre
        self.status = status
        self.reserved_by = reserved_by

class LibrarySystem:
    def __init__(self, filename: str = "books.txt"):
        self.filename = filename
        self.books: Dict[str, Book] = {}
        self.load_books()

    def parse_line(self, line: str) -> list:
        """Parse a line from the books file, handling quoted strings properly."""
        parts = []
        current = ''
        in_quotes = False
        
        for char in line.strip():
            if char == '"':
                if not in_quotes:  # Start of quoted string
                    in_quotes = True
                else:  # End of quoted string
                    in_quotes = False
                    if current:  # Add the quoted string if not empty
                        parts.append(current)
                        current = ''
            elif char == ' ' and not in_quotes:
                if current:  # Add non-quoted string if not empty
                    parts.append(current)
                    current = ''
            else:
                current += char
        
        if current:  # Add the last part if exists
            parts.append(current)
        
        return parts

    def load_books(self):
        """Load books from the file."""
        if not os.path.exists(self.filename):
            return
        
        with open(self.filename, 'r') as file:
            for line in file:
                parts = self.parse_line(line)
                if len(parts) >= 4:
                    id = parts[0]
                    title = parts[1]
                    author = parts[2]
                    genre = parts[3]
                    status = "Available"
                    reserved_by = None
                    
                    if len(parts) > 4:
                        status = parts[4]
                        if len(parts) > 5:
                            reserved_by = parts[5]
                    
                    self.books[id] = Book(id, title, author, genre, status, reserved_by)

    def save_books(self):
        """Save books to the file."""
        with open(self.filename, 'w') as file:
            for book in self.books.values():
                status_str = f"{book.status} {book.reserved_by}" if book.reserved_by else book.status
                file.write(f'{book.id} "{book.title}" "{book.author}" {book.genre} {status_str}\n')

    def display_books(self):
        """Display all books."""
        print("\n- - Available Books - -")
        print("ID      Title                   Author                  Genre        Status")
        print("-" * 80)
        for book in self.books.values():
            # Format each field with proper spacing
            id_field = f"{book.id:<8}"
            title_field = f"{book.title[:20]:<23}"
            author_field = f"{book.author[:20]:<22}"
            genre_field = f"{book.genre:<12}"
            
            status = book.status
            if book.reserved_by:
                status += f" by {book.reserved_by}"
            
            print(f"{id_field}{title_field}{author_field}{genre_field}{status}")

    def reserve_book(self, book_id: str, email: str) -> bool:
        """Reserve a book for a user."""
        if book_id not in self.books:
            print("❌ Book not found!")
            return False
        
        book = self.books[book_id]
        if book.status.lower() != "available":
            print("❌ Book is not available!")
            return False

        book.status = "Reserved"
        book.reserved_by = email
        self.save_books()
        return True

    def cancel_reservation(self, book_id: str, email: str) -> bool:
        """Cancel a book reservation."""
        if book_id not in self.books:
            print("❌ Book not found!")
            return False
        
        book = self.books[book_id]
        if book.status.lower() != "reserved" or book.reserved_by != email:
            print("❌ No reservation found for this book under your email!")
            return False

        book.status = "Available"
        book.reserved_by = None
        self.save_books()
        return True

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def main():
    library = LibrarySystem()
    
    while True:
        print("\n- - Community Library Management System - -")
        print("\n- - MAIN MENU - -")
        print("1 - Reserve a Book")
        print("2 - Cancel Reservation")
        print("3 - View All Books")
        print("Q - Quit")
        
        choice = input("Pick: ").strip().lower()
        
        if choice == 'q':
            print("📚 Exiting... Thank you for using the system!")
            break
            
        elif choice == '1':
            library.display_books()
            book_id = input("\nEnter the Book ID to reserve: ").strip()
            email = input("Enter your email: ").strip()
            
            if not validate_email(email):
                print("❌ Invalid email format!")
                continue
                
            if library.reserve_book(book_id, email):
                print(f"✅ The book has been reserved under {email}.")
            
        elif choice == '2':
            library.display_books()
            book_id = input("\nEnter the Book ID to cancel reservation: ").strip()
            email = input("Enter your email: ").strip()
            
            if not validate_email(email):
                print("❌ Invalid email format!")
                continue
                
            if library.cancel_reservation(book_id, email):
                print("✅ Reservation has been cancelled successfully.")
            
        elif choice == '3':
            library.display_books()
            
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main() 