The Library Management System is a web application designed to streamline and optimize the day-to-day operations of a local library. The project aims to provide librarians with a user-friendly platform to efficiently track books, manage their quantities, issue books to members, and handle book returns. The application is built using HTML, CSS, Flask, and SQL technologies.

The key functionalities of the Library Management System include:

<h3>Book and Member Management:</h3>Librarians can perform CRUD (Create, Read, Update, Delete) operations on books and members. They can add new books to the system, update book details such as title, author, and stock quantity, and manage member information.

Book Issuance and Returns: The system allows librarians to issue books to members. When a member borrows a book, the stock quantity is reduced accordingly. Members can also return books to the library, increasing the stock and triggering rent fees, if applicable.

Book Search: Librarians can search for books based on their titles and authors, enabling quick access to specific book information.

Rent Fee Calculation: The system calculates the rent fee for a book return based on the member's outstanding debt. It ensures that a member's debt does not exceed a maximum limit (Rs. 500).

The project's implementation involves creating HTML templates for various functionalities, designing a CSS style sheet for consistent and appealing user interfaces, and integrating Flask as the back-end framework to manage routing and database interactions. The SQL database is used to store book, member, and transaction data, enabling easy retrieval and modification.

Overall, the Library Management System aims to enhance the efficiency and organization of the library's processes, enabling librarians to manage books and members seamlessly, maintain accurate records, and ensure smooth book issuing and return transactions.
