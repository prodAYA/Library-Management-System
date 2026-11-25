from models.book import Book
from models.member import Member
from models.shelf import Shelf
from services.library import Library


def main() -> None:
    lib = Library("Gisma Campus Library")

    # 1. Create shelves and register them
    scifi_shelf = Shelf(shelf_id=1, genre="Sci-Fi", capacity=5)
    fantasy_shelf = Shelf(shelf_id=2, genre="Fantasy", capacity=5)
    lib.add_shelf(scifi_shelf)
    lib.add_shelf(fantasy_shelf)

    # 2. Create books and place them on shelves
    b1 = Book(101, "Dune", "Frank Herbert", "Sci-Fi")
    b2 = Book(102, "Neuromancer", "William Gibson", "Sci-Fi")
    b3 = Book(103, "Project Hail Mary", "Andy Weir", "Sci-Fi")
    b4 = Book(201, "The Hobbit", "J.R.R. Tolkien", "Fantasy")
    b5 = Book(202, "Mistborn", "Brandon Sanderson", "Fantasy")

    scifi_shelf.add_book(b1)
    scifi_shelf.add_book(b2)
    scifi_shelf.add_book(b3)
    fantasy_shelf.add_book(b4)
    fantasy_shelf.add_book(b5)

    # 3. Register members
    m1 = Member(1, "Alice", "alice@example.com")
    m2 = Member(2, "Bob", "bob@example.com")
    lib.register_member(m1)
    lib.register_member(m2)

    # 4. Run checkouts, a return (to test history), and a search
    lib.checkout_book(member_id=1, book_id=101)  # Alice borrows Dune
    lib.checkout_book(member_id=1, book_id=201)  # Alice borrows The Hobbit
    lib.checkout_book(member_id=2, book_id=102)  # Bob borrows Neuromancer

    # Bob returns Neuromancer (logs to Bob's history, marks book available)
    lib.return_book(member_id=2, book_id=102)

    print("--- Search for 'Sci-Fi' ---")
    for book in lib.search_books("Sci-Fi"):
        print(book)

    print("\n--- Shelf Stats ---")
    print(scifi_shelf.get_stats())
    print(fantasy_shelf.get_stats())

    # 5. Save everything to data/*.csv
    lib.save_all()
    print("\nSaved to CSV! Checking reload into a fresh Library instance...")

    # 6. Reload into a brand-new Library object to verify CSV round-trip
    reloaded_lib = Library("Gisma Campus Library")
    reloaded_lib.load_all()

    print("\n--- Reloaded Shelves ---")
    for s in reloaded_lib.shelves:
        print(s)
        for b in s.books:
            print("  ", b)

    print("\n--- Reloaded Members ---")
    for m in reloaded_lib.members:
        print(m, "| Summary:", m.get_summary(), "| History:", m.history)


if __name__ == "__main__":
    main()