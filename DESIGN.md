1. Overall Architecture
The Student Service Website is a web application built using Flask, a lightweight Python web framework. It uses SQLite as the database to store student information and feedback. The application follows a modular design with clear separation of concerns between different components such as routing, data handling, and front - end presentation.
2. Front - End Components
2.1 index.html
Purpose: This is the home page of the website. It provides two buttons for users to navigate to different sections: "Future Students (Q&A)" and "Current Students (Feedback)".
Design: The page has a background image of the campus main door. The buttons are centered on the page and have a semi - transparent background for better visibility.
2.2 qa.html
Purpose: This page is used for students to ask questions or query personal information. It displays the answer if available.
Design: It has a form where users can enter their question or student ID. The form is centered on the page with a semi - transparent background.
feedback.html
Purpose: This page allows current students to submit feedback about problems they encounter. It displays the submission status.
Design: It has a form with textarea for problem description and an input field for contact information. The form is centered on the page with a semi - transparent background.
3. Back - End Components
3.1 app.py
Purpose: This is the main Python file that runs the Flask application. It defines the routes, initializes the database, and implements the strategy pattern for handling different types of questions.
Design:
Routes:
/: Renders the index.html page.
/qa: Handles both GET and POST requests. For POST requests, it uses different strategies to find the answer to the question.
/feedback: Handles both GET and POST requests. For POST requests, it inserts the feedback into the database if the input is valid.
Strategy Pattern: It uses two strategies (StudentInfoStrategy and GeneralQAStrategy) to handle different types of questions. Each strategy has a handle method that returns the appropriate answer.
3.2 test_app.py
Purpose: This file contains unit tests for the application. It tests different user stories such as accessing the home page, querying personal information, handling invalid queries, and submitting feedback.
Design: It uses the unittest module in Python and the MagicMock class to mock database operations and other functions for testing purposes.
4. Database Design
students.db: This SQLite database has two tables:
students: Stores student information with columns student_id (primary key), name, and major.
feedbacks: Stores student feedback with columns id (primary key, auto - incremented), question, and contact.
