from models.book import Book
from models.shelf import Shelf
from models.member import Member
import csv


class Library:
    """Manages library inventory, member loans, and CSV file operations"""

    BOOK_FIELDS = [
        "book_id",
        "title",
        "author",
        "genre",
        "date_borrowed",
        "is_available",
    ]

    SHELF_FIELDS = ["shelf_id", "genre", "capacity", "book_ids"]

    MEMBER_FIELDS = ["member_id", "name", "email", "borrowed_books", "history"]

    def __init__(
        self,
        name,
        shelves: list[Shelf] | None = None,
        members: list[Member] | None = None,
    ):
        """Initialize a Library instance with shelves, members, and data path."""
        self.name = name
        self.shelves = shelves if shelves is not None else []
        self.members = members if members is not None else []

    def add_shelf(self, shelf: Shelf) -> None:
        """Register a new Shelf if its shelf_id does not already exist"""
        for existing_shelves in self.shelves:
            if shelf.shelf_id == existing_shelves.shelf_id:
                raise ValueError(
                    f"Shelf ID: {shelf.shelf_id} already exists in Library"
                )
        self.shelves.append(shelf)
        return

    def register_member(self, member: Member) -> None:
        """Register a new Member if their member_id doesnt already exist"""
        for existing_members in self.members:
            if member.member_id == existing_members.member_id:
                raise ValueError(
                    f"Shelf ID: {member.member_id} already exists in Library"
                )
        self.members.append(member)
        return

    def find_member(self, member_id: int) -> Member:
        """Return the Member matching member_id else raise ValueError."""
        for member in self.members:
            if member.member_id == member_id:
                return member
        raise ValueError(f"Member with ID {member_id} not found.")

    def find_book(self, book_id: int) -> Book:
        """Return the Book matching book_id across shelves else raise ValueError."""
        for shelf in self.shelves:
            for book in shelf.books:
                if book.book_id == book_id:
                    return book
        raise ValueError(f"Book with ID {book_id} not found in library.")

    def checkout_book(self, member_id: int, book_id: int) -> None:
        """
        Check out a Book to a registered Member if:
        - That member exists in the library record
        - The book exists in the Library record
        """
        current_member = self.find_member(member_id)
        target_book = self.find_book(book_id)
        current_member.borrow_book(target_book)
        return

    def return_book(self, member_id: int, book_id: int) -> None:
        """Process a book return for a registered (existing) Member"""
        current_member = self.find_member(member_id)
        current_member.return_book(book_id)
        return

    def search_books(self, query: str) -> list[Book]:
        """Search all Shelves in the Library to find books by Title, Author, or Genre"""
        result = []
        for shelf in self.shelves:
            for book in shelf.books:
                if book.matches_query(query):
                    result.append(book)
        return result

    def write_csv(
        self, filepath: str, fieldnames: list[str], rows: list[dict]
    ) -> None:
        """Write a list of serialized dictionaries to a CSV file."""
        with open(filepath, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def save_all(self) -> None:
        """Persist all books, shelves, and members to CSV files."""
        all_books = [
            book.to_dict() for shelf in self.shelves for book in shelf.books
        ]
        all_shelves = [shelf.to_dict() for shelf in self.shelves]
        all_members = [member.to_dict() for member in self.members]

        self.write_csv("data/books.csv", self.BOOK_FIELDS, all_books)
        self.write_csv("data/shelves.csv", self.SHELF_FIELDS, all_shelves)
        self.write_csv("data/members.csv", self.MEMBER_FIELDS, all_members)

    def load_all(self) -> None:
        """Load books, shelves, and members from CSV and re-link objects."""
        try:
            self.shelves.clear()
            self.members.clear()

            # Pass 1: Load all Book instances and index them by book_id
            books_by_id: dict[int, Book] = {}
            with open(
                "data/books.csv", mode="r", newline="", encoding="utf-8"
            ) as file:
                for row in csv.DictReader(file):
                    book = Book.from_dict(row)
                    books_by_id[book.book_id] = book

            # Pass 2: Load Shelves and re-attach Book references
            with open(
                "data/shelves.csv", mode="r", newline="", encoding="utf-8"
            ) as file:
                for row in csv.DictReader(file):
                    shelf = Shelf.from_dict(row)
                    raw_ids = row.get("book_ids", "")
                    if raw_ids:
                        for id_str in raw_ids.split(";"):
                            book = books_by_id.get(int(id_str))
                            if book:
                                shelf.add_book(book)
                    self.shelves.append(shelf)

            # Pass 3: Load Members and re-attach active borrowed Book references
            with open(
                "data/members.csv", mode="r", newline="", encoding="utf-8"
            ) as file:
                for row in csv.DictReader(file):
                    member = Member.from_dict(row)
                    raw_ids = row.get("borrowed_books", "")
                    if raw_ids:
                        for id_str in raw_ids.split(";"):
                            book = books_by_id.get(int(id_str))
                            if book:
                                member.borrowed_books.append(book)
                    self.members.append(member)
        except FileNotFoundError:
            # Start with an empty library if CSV files do not exist yet
            self.shelves.clear()
            self.members.clear()
