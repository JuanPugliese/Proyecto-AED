#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

class Book {
public:
    std::string title;
    std::string author;
    int year;
    std::string category;
    bool available;
    std::string borrower;
    int borrower_id;

    Book(const std::string& _title, const std::string& _author, int _year, const std::string& _category)
        : title(_title), author(_author), year(_year), category(_category), available(true) {}
};

class Library {
public:
    std::vector<Book> books;

    void addBook(const Book& book) {
        books.push_back(book);
    }

    Book* findBook(const std::string& title) {
        for (auto& book : books) {
            if (book.title == title) {
                return &book;
            }
        }
        return nullptr;
    }

    std::vector<Book*> searchByAuthor(const std::string& author) {
        std::vector<Book*> result;
        for (auto& book : books) {
            if (book.author == author) {
                result.push_back(&book);
            }
        }
        return result;
    }

    std::vector<Book*> searchByCategory(const std::string& category) {
        std::vector<Book*> result;
        for (auto& book : books) {
            if (book.category == category) {
                result.push_back(&book);
            }
        }
        return result;
    }

    std::vector<Book*> searchByYear(int year) {
        std::vector<Book*> result;
        for (auto& book : books) {
            if (book.year == year) {
                result.push_back(&book);
            }
        }
        return result;
    }

    std::vector<Book*> getAvailableBooks() {
        std::vector<Book*> result;
        for (auto& book : books) {
            if (book.available) {
                result.push_back(&book);
            }
        }
        return result;
    }

    void borrowBook(Book* book, const std::string& borrower, const int& borrower_id) {
        if (book) {
            if (book->available) {
                book->available = false;
                book->borrower = borrower;
                book->borrower_id = borrower_id;
                std::cout << "Book borrowed successfully." << std::endl;
            } else {
                std::cout << "Book is already borrowed." << std::endl;
            }
        } else {
            std::cout << "Book not found." << std::endl;
        }
    }

    void returnBook(Book* book, const std::string& borrower, const int& borrower_id) {
        if (book) {
            if (!book->available && book->borrower == borrower && book->borrower_id == borrower_id) {
                book->available = true;
                book->borrower_id = 0;
                std::cout << "Book returned successfully." << std::endl;
                std::cout << "Thank you " << book->borrower << " for returning the book" << std::endl;
                book->borrower = "";
            } else {
                std::cout << "The book has not been borrowed or the borrower id is incorrect." << std::endl;
            }
        } else {
            std::cout << "Book not found." << std::endl;
        }
    }
};

void sortByYear(std::vector<Book>& books) {
    std::sort(books.begin(), books.end(), [](const Book& a, const Book& b) {
        return a.year < b.year;
    });
}

void printBooks(const std::vector<Book*>& books) {
    for (const auto& book : books) {
        std::cout << "Title: " << book->title << std::endl;
        std::cout << "Author: " << book->author << std::endl;
        std::cout << "Year: " << book->year << std::endl;
        std::cout << "Category: " << book->category << std::endl;
        std::cout << "Available: " << (book->available ? "Yes" : "No") << std::endl;
        std::cout << "Borrower: " << book->borrower << std::endl;
        std::cout << std::endl;
    }
}

int main() {
    Library library;

    Book book1("The Catcher in the Rye", "J.D. Salinger", 1951, "Fiction");
    library.addBook(book1);

    Book book2("To Kill a Mockingbird", "Harper Lee", 1960, "Fiction");
    library.addBook(book2);

    Book book3("The Great Gatsby", "F. Scott Fitzgerald", 1925, "Fiction");
    library.addBook(book3);

    // Search by title
    Book* foundBook = library.findBook("The Great Gatsby");
    if (foundBook) {
        std::cout << "Book found!" << std::endl;
        // Do something with the book object
    } else {
        std::cout << "Book not found." << std::endl;
    }

    // Search by author
    std::vector<Book*> booksByAuthor = library.searchByAuthor("J.D. Salinger");
    if (!booksByAuthor.empty()) {
        std::cout << "Books by author found!" << std::endl;
        printBooks(booksByAuthor);
    } else {
        std::cout << "No books by author found." << std::endl;
    }

    // Search by category
    std::vector<Book*> booksByCategory = library.searchByCategory("Fiction");
    if (!booksByCategory.empty()) {
        std::cout << "Books by category found!" << std::endl;
        printBooks(booksByCategory);
    } else {
        std::cout << "No books by category found." << std::endl;
    }

    // Get available books
    std::vector<Book*> availableBooks = library.getAvailableBooks();
    if (!availableBooks.empty()) {
        std::cout << "Available books:" << std::endl;
        printBooks(availableBooks);
    } else {
        std::cout << "No available books." << std::endl;
    }

    // Borrow a book
    Book* bookToBorrow = library.findBook("The Catcher in the Rye");
    if (bookToBorrow) {
        std::string borrowerName = "John Smith"; // Borrower´s name
        int id = 1043634982; // Borrower´s ID
        library.borrowBook(bookToBorrow, borrowerName, id);
    } else {
        std::cout << "Book not found." << std::endl;
    }

    // Search by year
    std::vector<Book*> booksByYear = library.searchByYear(1951);
    if (!booksByYear.empty()) {
        std::cout << "Books by year found!" << std::endl;
        printBooks(booksByYear);
    } else {
        std::cout << "No books by year found." << std::endl;
    }

    // Return a book
    std::string borrowerName = "John Smith"; // Borrower
    int id = 1043634982; // Borrower´s ID
    Book* bookToReturn = library.findBook("The Catcher in the Rye");

    if (bookToReturn) {
        library.returnBook(bookToReturn, borrowerName, id);
    } else {
        std::cout << "Book not found." << std::endl;
    }

    std::cout << "Presiona enter para salir...";
    std::cin.ignore();  // Ignorar el carácter ingresado

    return 0;
}

