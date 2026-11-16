from models.book import Book


class Shelf:

    def __init__(
        self,
        shelf_id: int,
        genre: str,
        capacity: int,
        books: list[Book] = books if books is not None else [],
    ):
        """Initialize an instance of a Shelf object"""
        self.shelf_id = shelf_id
        self.genre = genre
        self.capacity = capacity
        self.books = books

    @classmethod
    def from_dict(cls, data: dict):
        """
        Construct an Instance of a Shelf object using a dict import (from a CSV file)
        This method does not handle populating shelf objects with book objects
        load_all() from the Library class handles adding books to shlef objects after both have been created
        """
        return cls(
            shelf_id=int(data["shelf_id"]),
            genre=data["genre"],
            capacity=int(data["capacity"]),
        )

    def __str__(self):
        """return a string representation of a shelf object"""
        return f"[{self.shelf_id}] {self.genre} Shelf - Capacity: {self.capacity}, Books: {len(self.books) if self.books else 0}"

    def add_book(self, book: Book):
        """
        Add a Book Object to the SHelf, raise appropriate errors if:
        - The book is already on the shelf
        - The shelf is at max capacity
        """
        flag = False
        for existing_book in self.books:
            if existing_book.book_id == book.book_id:
                flag = True
                break

        if flag:
            raise ValueError(
                f"Book '{book.title}' (Book ID: {book.book_id}) is already on the shelf."
            )

        elif len(self.books) == self.capacity:
            raise ValueError(
                f"Shelf '{self.genre}' (Shelf ID: {self.shelf_id}) is at full capacity."
            )

        elif self.genre.lower() != book.genre.lower():
            raise ValueError(
                f"Book '{book.title}' (Book ID: {book.book_id}) genre '{book.genre}' does not match shelf genre '{self.genre}'."
            )

        else:
            self.books.append(book)

    def remove_book(self, book_id):
        """
        Remove a Book Object from a Shelf, raise appropriate errors if:
        - The book is not on the shelf
        - The shelf is already empty
        """
        if not self.books:
            raise ValueError(
                f"Shelf '{self.genre}' (Shelf ID: {self.shelf_id}) is empty. No books to remove."
            )

        removed = False

        for existing_book in self.books:
            if existing_book.book_id == book_id:
                self.books.remove(existing_book)
                removed = True
                break

        if not removed:
            raise ValueError(
                f"Book with ID '{book_id}' is not on the shelf '{self.genre}' (Shelf ID: {self.shelf_id})."
            )

    def get_available_books(self):
        """Return a list of the books on the SHelf that are currently available"""
        return [book for book in self.books if book.is_available]

    def get_stats(self):
        """
        Return a dictionary of the Shelf's statistics including:
        - Shelf ID
        - Genre
        - Total Books
        - Available Books
        - Capacity
        - Occupancy Percentage
        """
        return {
            "shelf_id": self.shelf_id,
            "genre": self.genre,
            "total_books": len(self.books),
            "available_books": len(self.get_available_books()),
            "capacity": self.capacity,
            "occupancy_percentage": (len(self.books) / self.capacity * 100),
        }

    def to_dict(self) -> dict:
        """Convert the shelf instance to a dictionary representation for CSV export."""
        book_list = ";".join(str(book.book_id) for book in self.books)
        return {
            "shelf_id": self.shelf_id,
            "genre": self.genre,
            "capacity": self.capacity,
            "books": book_list,
        }
