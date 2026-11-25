from models.book import Book
from datetime import datetime
import json


class Member:
    """Represents Objects of the Member Class"""

    def __init__(
        self,
        member_id: int,
        name: str,
        email: str,
        borrowed_books: list[Book] | None = None,
        history: list[dict] | None = None,
    ):
        """Create an Instance of the Member class with the following attributes"""
        self.member_id = member_id
        self.name = name
        self.email = email
        self.borrowed_books = (
            borrowed_books if borrowed_books is not None else []
        )
        self.history = history if history is not None else []

    @classmethod
    def from_dict(cls, data: dict):
        """Initialize an instance of the Member Class using a dict from a CSV Import"""
        history = data.get("history")
        parsed_history = json.loads(history) if history else []
        return cls(
            member_id=int(data["member_id"]),
            name=str(data["name"]),
            email=str(data["email"]),
            history=parsed_history,
        )

    def __str__(self):
        """Represent an Object of the Member class with a String"""
        return f"{self.name} has Member ID: {self.member_id} and email: {self.email}"

    def has_borrowed(self, book_id: int) -> bool:
        """Checks whether a Member has a specific book using book_id"""
        for borrowed in self.borrowed_books:
            if borrowed.book_id == book_id:
                return True
        return False

    def borrow_book(self, book: Book) -> None:
        """Adds a Book to a Member's possession if they do not already have it"""
        if not self.has_borrowed(book.book_id):
            book.check_out()
            self.borrowed_books.append(book)
        else:
            raise ValueError(
                f"{self.member_id} is already borrowing {book.title}"
            )

    def return_book(self, book_id: int) -> None:
        """
        - Takes a Book out of a Member's posession if they have it
        - raises an error if that book is not being borrowed ny the Member
        - saves a record of that lease in that member's History
        - returns that Book to make it available again
        """
        for book in self.borrowed_books:
            if book_id == book.book_id:
                borrow_date = (
                    book.date_borrowed.isoformat()
                    if book.date_borrowed
                    else ""
                )
                self.history.append(
                    {
                        "book_id": book.book_id,
                        "title": book.title,
                        "borrowed_at": borrow_date,
                        "returned_at": datetime.now().isoformat(),
                    }
                )
                book.return_book()
                self.borrowed_books.remove(book)
                return
        raise ValueError(
            f"Book ID: {book_id} is not currently being borrowed by {self.name}"
        )

    def get_summary(self) -> dict:
        """Returns a dict containing statistics about a Member"""
        return {
            "member_id": self.member_id,
            "name": self.name,
            "email": self.email,
            "books_currently_borrowing": len(self.borrowed_books),
            "books_borrowed": len(self.history),
        }

    def to_dict(self) -> dict:
        """Serializes a Member Object into a dict for CSV Export"""
        borrowed_book_ids = ";".join(
            str(book.book_id) for book in self.borrowed_books
        )
        return {
            "member_id": self.member_id,
            "name": self.name,
            "email": self.email,
            "borrowed_books": borrowed_book_ids,
            "history": json.dumps(self.history),
        }
