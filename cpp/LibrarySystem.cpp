#include "MainHeader.h"

int main() {
    Library library;
    loadBooksFromFile(library, "books.txt");

    int choice;
    do {
        std::cout << "Library System\n"
                  << "1. Add Book\n"
                  << "2. Remove Book\n"
                  << "3. Search Book\n"
                  << "4. Display Books\n"
                  << "5. Checkout Book\n"
                  << "6. Return Book\n"
                  << "7. Save & Exit\n"
                  << "Enter choice: ";
        std::cin >> choice;

        std::string title, author, ISBN;
        int year;
        bool isAvailable;

        switch (choice) {
            case 1:
                std::cout << "Enter title, author, ISBN, year, availability (1/0): ";
                std::cin >> title >> author >> ISBN >> year >> isAvailable;
                library.addBook(Book(title, author, ISBN, year, isAvailable));
                break;
            case 2:
                std::cout << "Enter ISBN to remove: ";
                std::cin >> ISBN;
                library.removeBook(ISBN);
                break;
            case 3:
                std::cout << "Enter title to search: ";
                std::cin >> title;
                library.searchBookByTitle(title);
                break;
            case 4:
                library.displayBooks();
                break;
            case 5:
                std::cout << "Enter ISBN to checkout: ";
                std::cin >> ISBN;
                checkoutBook(library, ISBN);
                break;
            case 6:
                std::cout << "Enter ISBN to return: ";
                std::cin >> ISBN;
                returnBook(library, ISBN);
                break;
            case 7:
                saveBooksToFile(library, "books.txt");
                std::cout << "Books saved. Exiting...\n";
                break;
            default:
                std::cout << "Invalid choice.\n";
        }
    } while (choice != 7);
    const size_t arena_size = 1024;  
    ArenaAllocator arena(arena_size);
    ExampleObject* obj1 = new (arena.allocate(sizeof(ExampleObject))) ExampleObject(1, 3.14);
    ExampleObject* obj2 = new (arena.allocate(sizeof(ExampleObject))) ExampleObject(2, 6.28);
    ExampleObject* obj3 = new (arena.allocate(sizeof(ExampleObject))) ExampleObject(3, 9.42);
    obj1->print();
    obj2->print();
    obj3->print();
    arena.reset();
    ExampleObject* obj4 = new (arena.allocate(sizeof(ExampleObject))) ExampleObject(4, 12.56);
    obj4->print();




    return 0;
}
