import datetime

class Book:
    """Represents a Book Instance in the Library"""

    def __init__(
        self,
        book_id: int,
        title: str,
        author: str,
        genre: str,
        date_borrowed: datetime.datetime | None = None,
        is_available: bool = True,
    ):
        """Initialize a book instance with the given attributes."""
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.date_borrowed = date_borrowed
        self.is_available = is_available

    @classmethod
    def from_dict(cls, data: dict):
        """Construct a book from a dict import (from a CSV file)"""
        date_borrowed = data.get("date_borrowed", "")
        parsed_date = (
            datetime.datetime.fromisoformat(date_borrowed)
            if date_borrowed
            else None
        )
        return cls(
            book_id=int(data["book_id"]),
            title=data["title"],
            author=data["author"],
            genre=data["genre"],
            date_borrowed=parsed_date,
            is_available=str(data["is_available"]).lower() == "true",
        )
    
    def __str__(self) -> str:
        """Return a string representation of the book instance."""
        status = (
            "Available"
            if self.is_available
            else f"Checked out ({self.date_borrowed:%Y-%m-%d})"
        )
        return f"[{self.book_id}] {self.title} by {self.author} ({self.genre}) - {status}"

    def check_out(self) -> None:
        """Mark the book as checked out with the current time stamped as the date borrowed."""
        if self.is_available:
            self.is_available = False
            self.date_borrowed = datetime.datetime.now()
        else:
            raise ValueError(
                f"Book '{self.title}' (Book ID: {self.book_id}) is not in stock."
            )

    def return_book(self) -> None:
        """Return the book and mark it as available."""
        if not self.is_available:
            self.is_available = True
            self.date_borrowed = None
        else:
            raise ValueError(
                f"Book '{self.title}' (Book ID: {self.book_id}) is already available in stock."
            )

    def matches_query(self, query) -> bool:
        """Check if the book matches the given query in title, author, or genre."""
        formatted_query = query.strip().lower()
        return (
            formatted_query in self.title.lower()
            or formatted_query in self.author.lower()
            or formatted_query in self.genre.lower()
        )

    def to_dict(self) -> dict:
        """Convert the book instance to a dictionary representation for CSV export."""
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "date_borrowed": (
                self.date_borrowed.isoformat() if self.date_borrowed else ""
            ),
            "is_available": "True" if self.is_available else "False",
        }

    
