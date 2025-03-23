#include "MainHeader.h"
Book::Book(const std::string& title, const std::string& author, const std::string& ISBN, int year, bool isAvailable)
    : title(title), author(author), ISBN(ISBN), year(year), isAvailable(isAvailable) {}

std::string Book::getTitle() const { return title; }
std::string Book::getAuthor() const { return author; }
std::string Book::getISBN() const { return ISBN; }
int Book::getYear() const { return year; }
bool Book::getAvailability() const { return isAvailable; }
void Book::setAvailability(bool available) { isAvailable = available; }
void Book::displayBook() const {
    std::cout << "Title: " << title << ", Author: " << author << ", ISBN: " << ISBN
              << ", Year: " << year << ", Available: " << (isAvailable ? "Yes" : "No") << '\n';
}

void Library::addBook(const Book& book) { books.push_back(book); }
void Library::removeBook(const std::string& ISBN) {
    for (auto it = books.begin(); it != books.end(); ++it) {
        if (it->getISBN() == ISBN) {
            books.erase(it);
            break;
        }
    }
}

void Library::searchBookByTitle(const std::string& title) const {
    for (const auto& book : books) {
        if (book.getTitle() == title) {
            book.displayBook();
            return;
        }
    }
    std::cout << "Book not found.\n";
}

void Library::displayBooks() const {
    for (const auto& book : books) {
        book.displayBook();
    }
}

Book* Library::findBookByISBN(const std::string& ISBN) {
    for (auto& book : books) {
        if (book.getISBN() == ISBN) {
            return &book;
        }
    }
    return nullptr;
}

void loadBooksFromFile(Library& library, const std::string& filename) {
    std::ifstream file(filename);
    if (!file) return;

    std::string title, author, ISBN;
    int year;
    bool isAvailable;
    while (file >> title >> author >> ISBN >> year >> isAvailable) {
        library.addBook(Book(title, author, ISBN, year, isAvailable));
    }
}

void saveBooksToFile(const Library& library, const std::string& filename) {
    std::ofstream file(filename);
    if (!file) {
        std::cerr << "Error: Unable to open file " << filename << " for writing.\n";
        return;
    }
    for (const auto& book : library.books) {
        file << book.getTitle() << '\n' << book.getAuthor() << '\n' << book.getISBN() << '\n'
             << book.getYear() << '\n' << book.getAvailability() << '\n';
    }
}


void checkoutBook(Library& library, const std::string& ISBN) {
    Book* book = library.findBookByISBN(ISBN);
    if (book && book->getAvailability()) {
        book->setAvailability(false);
        std::cout << "Book checked out successfully.\n";
    } else {
        std::cout << "Book is not available for checkout.\n";
    }
}

void returnBook(Library& library, const std::string& ISBN) {
    Book* book = library.findBookByISBN(ISBN);
    if (book && !book->getAvailability()) {
        book->setAvailability(true);
        std::cout << "Book returned successfully.\n";
    } else {
        std::cout << "Invalid return request.\n";
    }
}

