from PyQt5 import QtWidgets, QtGui, QtCore
from book_library import Book, EBook, Library, BookNotAvailableError
import sys

class LibraryManagementApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.library = Library()
        self.setWindowTitle("Library Management System")
        self.setGeometry(200, 100, 800, 600)
        self.initUI()

    def initUI(self):
        main_widget = QtWidgets.QWidget()
        self.setCentralWidget(main_widget)
        layout = QtWidgets.QVBoxLayout()

        # Input Group
        input_group = QtWidgets.QGroupBox("Add New Book")
        input_layout = QtWidgets.QFormLayout()

        self.title_input = QtWidgets.QLineEdit()
        self.author_input = QtWidgets.QLineEdit()
        self.isbn_input = QtWidgets.QLineEdit()
        self.ebook_check = QtWidgets.QCheckBox("eBook?")
        self.size_input = QtWidgets.QLineEdit()
        self.size_input.setDisabled(True)
        self.ebook_check.stateChanged.connect(self.toggle_ebook_fields)

        input_layout.addRow("Title:", self.title_input)
        input_layout.addRow("Author:", self.author_input)
        input_layout.addRow("ISBN:", self.isbn_input)
        input_layout.addRow(self.ebook_check)
        input_layout.addRow("Download Size (MB):", self.size_input)

        add_button = QtWidgets.QPushButton("Add Book")
        add_button.clicked.connect(self.add_book)
        input_layout.addRow(add_button)

        clear_button = QtWidgets.QPushButton("Clear Fields")
        clear_button.clicked.connect(self.clear_fields)
        input_layout.addRow(clear_button)

        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # Action Group
        action_group = QtWidgets.QGroupBox("Book Actions")
        action_layout = QtWidgets.QVBoxLayout()
        lend_button = QtWidgets.QPushButton("Lend Book")
        lend_button.clicked.connect(self.lend_book)
        return_button = QtWidgets.QPushButton("Return Book")
        return_button.clicked.connect(self.return_book)
        remove_button = QtWidgets.QPushButton("Remove Book")
        remove_button.clicked.connect(self.remove_book)
        author_button = QtWidgets.QPushButton("View Books by Author")
        author_button.clicked.connect(self.view_books_by_author)
        
        action_layout.addWidget(lend_button)
        action_layout.addWidget(return_button)
        action_layout.addWidget(remove_button)
        action_layout.addWidget(author_button)
        action_group.setLayout(action_layout)
        layout.addWidget(action_group)

        # List Group
        self.book_list = QtWidgets.QListWidget()
        layout.addWidget(self.book_list)

        main_widget.setLayout(layout)
        self.update_book_list()

    def toggle_ebook_fields(self):
        self.size_input.setDisabled(not self.ebook_check.isChecked())
        if not self.ebook_check.isChecked():
            self.size_input.clear()

    def clear_fields(self):
        self.title_input.clear()
        self.author_input.clear()
        self.isbn_input.clear()
        self.ebook_check.setChecked(False)
        self.size_input.clear()

    def add_book(self):
        title = self.title_input.text().strip()
        author = self.author_input.text().strip()
        isbn = self.isbn_input.text().strip()
        size = self.size_input.text().strip()

        if not title or not author or not isbn:
            self.show_error("Error", "Title, Author, and ISBN are required.")
            return

        try:
            if self.ebook_check.isChecked():
                if not size or float(size) <= 0:
                    self.show_error("Error", "Download size must be a positive number.")
                    return
                book = EBook(title, author, isbn, float(size))
            else:
                book = Book(title, author, isbn)
            self.library.add_book(book)
            self.update_book_list()
            self.show_message("Success", f"Book '{title}' added successfully.")
            self.clear_fields()
        except Exception as e:
            self.show_error("Error", str(e))

    def lend_book(self):
        isbn, ok = QtWidgets.QInputDialog.getText(self, "Lend Book", "Enter ISBN of the book to lend:")
        if ok and isbn.strip():
            try:
                self.library.lend_book(isbn.strip())
                self.update_book_list()
                self.show_message("Success", "Book lent successfully.")
            except BookNotAvailableError as e:
                self.show_error("Error", str(e))

    def return_book(self):
        isbn, ok = QtWidgets.QInputDialog.getText(self, "Return Book", "Enter ISBN of the book to return:")
        if ok and isbn.strip():
            try:
                self.library.return_book(isbn.strip())
                self.update_book_list()
                self.show_message("Success", "Book returned successfully.")
            except BookNotAvailableError as e:
                self.show_error("Error", str(e))

    def remove_book(self):
        isbn, ok = QtWidgets.QInputDialog.getText(self, "Remove Book", "Enter ISBN of the book to remove:")
        if ok and isbn.strip():
            self.library.remove_book(isbn.strip())
            self.update_book_list()
            self.show_message("Success", "Book removed successfully.")

    def view_books_by_author(self):
        author, ok = QtWidgets.QInputDialog.getText(self, "View Books by Author", "Enter author's name:")
        if ok and author.strip():
            books = list(self.library.books_by_author(author.strip()))
            if books:
                self.book_list.clear()
                self.book_list.addItem(f"Books by {author.strip()}:")
                for book in books:
                    self.book_list.addItem(str(book))
            else:
                self.show_error("Not Found", "No books found by this author.")

    def update_book_list(self):
        self.book_list.clear()
        self.book_list.addItem("Available Books:")
        for book in self.library:
            self.book_list.addItem(str(book))

    def show_message(self, title, message):
        QtWidgets.QMessageBox.information(self, title, message)

    def show_error(self, title, message):
        QtWidgets.QMessageBox.critical(self, title, message)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = LibraryManagementApp()
    window.show()
    sys.exit(app.exec_())
