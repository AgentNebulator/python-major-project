# Week 15: Final Project
# Code by team of Mathias Laven, Ethan Smith, Kathleen Brozynski (05/15/2024)

import sqlite3
import student_data
import tkinter
import tkinter.ttk
from tkinter import END

# Relevant constants

TITLE_TEXT = "Student Records Database"
TITLE_FONT = "Helvetica 12 bold"

DISPLAY_DEFAULT = "Enter new Student ID to add data or existing ID to edit/delete data"

ERROR_ID_EMPTY = "Error: Student ID is required"
ERROR_ID_NOT_FOUND = "Error: No student found with that ID"
ERROR_ID_ALREADY_EXISTS = 'Error: Student already exists with that ID'
ERROR_ID_WRONG_LENGTH = "Error: Student ID must be 5 characters in length"
ERROR_ID_NOT_INT = 'Error: Student ID must be an integer'

ERROR_FIELD_EMPTY = "Error: No value entered for {0}"
ERROR_NO_EDITS_MADE = "Error: All fields empty, no edits are being made"

ERROR_SCHOOL_YEAR_NOT_INT = 'Error: School Year must be an integer'
ERROR_COURSE_ID_NOT_INT = 'Error: Course ID must be an integer'

ERROR_DEFAULT = 'Error: Database manipulation failed, please try again'

FIELD_TITLES = ["Student ID", "Last Name", "First Name", "School Year", "Course Name", "Course ID", "Professor Name"]

TABLE_COLUMN_WIDTH = 100

# Main function
def main():
    # Connect to the database
    conn = sqlite3.connect('student_database.db')
    cur = conn.cursor()

    # Create table of students
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS Students (student_id INTEGER PRIMARY KEY NOT NULL, last_name TEXT, 
        first_name TEXT, school_year INTEGER, course_name TEXT, course_ID INTEGER, professor_name TEXT)'''
    )

    # Enter default data
    cur.executemany('INSERT OR IGNORE INTO Students VALUES (?, ?, ?, ?, ?, ?, ?)', student_data.data)

    # Close the connection
    conn.commit()
    conn.close()


# Create Class for GUI
class StudentDatabaseGUI:
    # Use variable data_table from main() to show table
    def __init__(self):
        # Connect to the database
        conn = sqlite3.connect('student_database.db')
        cur = conn.cursor()

        # Select the data and extract results
        cur.execute('SELECT * FROM Students')
        data = cur.fetchall()  # data is the data in the table, excluding headers

        # Store results as a tuple
        self.__data = data

        # Close connection
        conn.close()

        # Initiate main window, frames, and labels
        self.__main_window = tkinter.Tk()
        self.__main_window.title("Student Records Database")

        # Create frames
        self.__title_frame = tkinter.Frame(self.__main_window)
        self.__treeview_frame = tkinter.Frame(self.__main_window)
        self.__treeview_separator = tkinter.ttk.Separator(self.__main_window, orient="horizontal")
        self.__label_frame = tkinter.Frame(self.__main_window)
        self.__id_entry_frame = tkinter.Frame(self.__main_window)
        self.__id_entry_separator = tkinter.ttk.Separator(self.__main_window, orient="horizontal")
        self.__student_entry_frame = tkinter.Frame(self.__main_window)
        self.__course_entry_frame = tkinter.Frame(self.__main_window)
        self.__data_entry_separator = tkinter.ttk.Separator(self.__main_window, orient="horizontal")
        self.__button_frame = tkinter.Frame(self.__main_window)

        # Create window title
        self.__title_label = tkinter.Label(self.__title_frame, text=TITLE_TEXT, font=TITLE_FONT)

        # Create data table (well, treeview)
        # Treeview information sourced from https://pythonguides.com/python-tkinter-table-tutorial/
        self.__data_treeview = tkinter.ttk.Treeview(self.__treeview_frame)

        # Set the headers to the data headers
        self.__data_treeview['columns'] = FIELD_TITLES

        # Set the default columns and headings to not show
        self.__data_treeview.column("#0", width=0, stretch=False)
        self.__data_treeview.heading("#0", anchor="center")

        # Format columns and headings
        for header in FIELD_TITLES:
            self.__data_treeview.column(header, anchor="center", width=TABLE_COLUMN_WIDTH)
            self.__data_treeview.heading(header, text=header, anchor="center")

        # Insert data
        for student in data:
            self.__data_treeview.insert(parent='', index='end', values=student)

        # Create label text for special requested data
        self.__displayed_data = tkinter.StringVar()
        self.__displayed_data.set(DISPLAY_DEFAULT)

        # Create label and format with text
        self.__data_label = tkinter.Label(self.__label_frame,
                                          textvariable=self.__displayed_data, )

        # Create labels and entry boxes for student info
        self.__student_ID_label = tkinter.Label(self.__id_entry_frame, text=f"{FIELD_TITLES[0]}: ")
        self.__student_ID_entry = tkinter.Entry(self.__id_entry_frame)

        self.__last_label = tkinter.Label(self.__student_entry_frame, text=f"{FIELD_TITLES[1]}: ", width=12, anchor="e")
        self.__last_entry = tkinter.Entry(self.__student_entry_frame)

        self.__first_label = tkinter.Label(self.__student_entry_frame, text=f"{FIELD_TITLES[2]}: ", width=10,
                                           anchor="e")
        self.__first_entry = tkinter.Entry(self.__student_entry_frame)

        self.__year_label = tkinter.Label(self.__student_entry_frame, text=f"{FIELD_TITLES[3]}: ", width=13, anchor="e")
        self.__year_entry = tkinter.Entry(self.__student_entry_frame)

        self.__course_name_label = tkinter.Label(self.__course_entry_frame, text=f"{FIELD_TITLES[4]}: ", width=12,
                                                 anchor="e")
        self.__course_name_entry = tkinter.Entry(self.__course_entry_frame)

        self.__course_ID_label = tkinter.Label(self.__course_entry_frame, text=f"{FIELD_TITLES[5]}: ", width=10,
                                               anchor="e")
        self.__course_ID_entry = tkinter.Entry(self.__course_entry_frame)

        self.__professor_label = tkinter.Label(self.__course_entry_frame, text=f"{FIELD_TITLES[6]}: ", width=13,
                                               anchor="e")
        self.__professor_entry = tkinter.Entry(self.__course_entry_frame)

        # Create button to show program instructions
        self.__help_button = tkinter.Button(self.__button_frame,
                                            text='Help',
                                            command=self.__help_menu)

        # Create button to add data
        self.__add_button = tkinter.Button(self.__button_frame,
                                           text='Add Student',
                                           command=self.__add_data)

        # Create button to edit data by ID
        self.__edit_button = tkinter.Button(self.__button_frame,
                                            text='Edit Student',
                                            command=self.__edit_data)

        # Create button to delete data by ID
        self.__delete_button = tkinter.Button(self.__button_frame,
                                              text='Delete Student',
                                              command=self.__delete_data)

        # Create exit button for user-friendly exit
        self.__exit_button = tkinter.Button(self.__button_frame,
                                            text='Exit',
                                            command=self.__main_window.destroy)

        # Pack elements
        self.__title_label.pack(pady=0)

        self.__data_treeview.pack()
        self.__data_label.pack()

        self.__student_ID_label.pack(side="left")
        self.__student_ID_entry.pack(side="left")

        self.__last_label.grid(column=0, row=0)
        self.__last_entry.grid(column=1, row=0)

        self.__first_label.grid(column=2, row=0)
        self.__first_entry.grid(column=3, row=0)

        self.__year_label.grid(column=4, row=0)
        self.__year_entry.grid(column=5, row=0)

        self.__course_name_label.grid(column=0, row=1)
        self.__course_name_entry.grid(column=1, row=1)

        self.__course_ID_label.grid(column=2, row=1)
        self.__course_ID_entry.grid(column=3, row=1)

        self.__professor_label.grid(column=4, row=1)
        self.__professor_entry.grid(column=5, row=1)

        self.__help_button.pack(side="left", padx=5)
        self.__add_button.pack(side="left", padx=5)
        self.__edit_button.pack(side="left", padx=5)
        self.__delete_button.pack(side="left", padx=5)
        self.__exit_button.pack(side='left', padx=5)

        self.__title_frame.pack(padx=(10, 10), pady=(10, 5))

        self.__treeview_frame.pack(padx=(10, 10), pady=(10, 10))
        self.__treeview_separator.pack(fill="x", pady=(10, 10))

        self.__label_frame.pack(padx=(40, 40), pady=(5, 5))
        self.__id_entry_frame.pack(padx=(40, 40), pady=(10, 10))
        self.__id_entry_separator.pack(fill="x", pady=(5, 5))

        self.__student_entry_frame.pack(padx=(40, 40), pady=(5, 5))
        self.__course_entry_frame.pack(padx=(40, 40), pady=(5, 5))
        self.__data_entry_separator.pack(fill="x", pady=(5, 5))

        self.__button_frame.pack(padx=(40, 40), pady=(10, 40))

        # Main loop
        tkinter.mainloop()

    def __help_menu(self):
        # Create help window
        self.__help_window = tkinter.Toplevel(self.__main_window)
        self.__help_window.title("Student Records Database - Help Menu")

        # Set help text
        help_text = (
            "This is an interface for managing student records.",
            "",
            "The interface displays a table with sample data of students already provided. The table is ",
            "organized by the headings above and uses the Student ID to identify each row. ",
            "If you do not see all the student data, you may need to scroll.",
            "",
            "The entry fields are used in conjunction with the buttons to add, edit, ",
            "and delete student data.",
            "",
            "To add a student, enter the Student ID and other data into the fields, ",
            "then press Add Student.",
            "",
            "To edit a student record, enter the Student ID and new data into its ",
            "corresponding fields, then press Edit Student. ",
            "",
            "To delete a student, you only need to use the Student ID."
        )

        # Join help text for use, with a line break between each
        joined_help_text = "\n".join(help_text)

        # Create frame and label for help text
        self.__help_frame = tkinter.Frame(self.__help_window)
        self.__help_label = tkinter.Label(self.__help_frame, text=joined_help_text, anchor="center")

        # Pack frame and label
        self.__help_frame.pack()
        self.__help_label.pack(padx=20, pady=20)

    def __add_data(self):
        # Get data from entry fields
        requested_sID, requested_values = self.__get_entered_data()

        # Confirm data is not invalid
        if not self.__check_data_valid(requested_sID, requested_values, False):
            return

        # Connect to database
        conn = sqlite3.connect('student_database.db')
        cur = conn.cursor()

        # Test if every value is present
        if all(requested_values):
            try:
                # Add row with those values
                cur.execute('''INSERT INTO Students (student_id, last_name, first_name, school_year, 
                                    course_name, course_ID, professor_name) VALUES (?,?,?,?,?,?,?) ''',
                            requested_values)

                conn.commit()

                self.__displayed_data.set('The student was added.')

                # Update GUI table
                self.__update_treeview()
                self.__clear_box()

            # If table field does not match correct int type
            except sqlite3.IntegrityError:
                cur.execute('''SELECT student_id From Students
                            WHERE student_id == ?''', (requested_sID,))
                results = cur.fetchone()

                if results:
                    self.__displayed_data.set(ERROR_ID_ALREADY_EXISTS)
                else:
                    self.__displayed_data.set(ERROR_DEFAULT)

        else:
            # Check which value is not present
            # (iterating backwards so the first unfilled field shows up, not the last)
            for i in range(len(requested_values) - 1, -1, -1):
                if not requested_values[i]:
                    self.__displayed_data.set(ERROR_FIELD_EMPTY.format(FIELD_TITLES[i]))

        # Close connection
        conn.close()

    def __edit_data(self):
        # Get data from entry fields
        requested_sID, requested_values = self.__get_entered_data()

        # Connect to database
        conn = sqlite3.connect('student_database.db')
        cur = conn.cursor()

        # Get student with entered ID
        cur.execute('''SELECT * From Students
                    WHERE student_id == ?''', (requested_sID,))
        results = cur.fetchone()

        # Confirm data is not invalid
        if not self.__check_data_valid(requested_sID, requested_values, results):
            return

        # Test if any fields are filled past the student ID
        if not any(requested_values[1:]):
            self.__displayed_data.set(ERROR_NO_EDITS_MADE)
            return

        try:
            # Create list out of current data (to be overwritten)
            new_database_data = list(results)

            for i in range(len(requested_values)):
                # Only overwrite existing data if field has new content
                if requested_values[i]:
                    new_database_data[i] = requested_values[i]

            # Move ID to last position
            new_database_data = new_database_data[1:] + [new_database_data[0]]

            cur.execute('''UPDATE Students SET 
                                    last_name = ?,
                                    first_name = ?,
                                    school_year = ?,
                                    course_name = ?,
                                    course_id = ?,
                                    professor_name = ?
                                WHERE student_id == ?''', new_database_data)

            conn.commit()

            self.__displayed_data.set('The student was edited.')

            # Call update_treeview to update GUI and clear entry boxes
            self.__update_treeview()
            self.__clear_box()

        # If an error occurs
        except:
            self.__displayed_data.set(ERROR_DEFAULT)

        # Close connection
        conn.close()

    def __delete_data(self):
        # Connect to database
        conn = sqlite3.connect('student_database.db')
        # Get the input from the entry box
        cur = conn.cursor()
        # Use that input to find the row in the database
        requested_id = self.__student_ID_entry.get()

        # Try and find data
        cur.execute('''SELECT student_id From Students
                    WHERE student_id == ?''', (requested_id,))
        results = cur.fetchone()

        # If data isn't found, stop execution
        if not results:
            self.__displayed_data.set(ERROR_ID_NOT_FOUND)
            return False

        try:
            # Delete data
            cur.execute('''DELETE FROM Students
                                WHERE student_id == ?''',
                        (requested_id,))

            conn.commit()

            self.__displayed_data.set('The student was deleted.')

            # Call update_treeview to update GUI and clear boxes
            self.__update_treeview()
            self.__clear_box()

        # If an error occurs
        except:
            self.__displayed_data.set(ERROR_DEFAULT)

        # Close connection
        conn.close()

    def __update_treeview(self):
        # Clear the existing data in the treeview
        for item in self.__data_treeview.get_children():
            self.__data_treeview.delete(item)

        # Re-fetch and re-insert the data from the database
        conn = sqlite3.connect('student_database.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM Students')
        data = cur.fetchall()

        for student in data:
            self.__data_treeview.insert(parent='', index='end', values=student)

        # Close connection
        conn.close()

    # Get users input in the GUI
    def __get_entered_data(self):
        requested_sID = self.__student_ID_entry.get()
        requested_last = self.__last_entry.get()
        requested_first = self.__first_entry.get()
        requested_year = self.__year_entry.get()
        requested_cname = self.__course_name_entry.get()
        requested_cID = self.__course_ID_entry.get()
        requested_professor = self.__professor_entry.get()

        requested_values = (requested_sID, requested_last, requested_first, requested_year, requested_cname,
                            requested_cID, requested_professor)

        return requested_sID, requested_values

    # Clear all entries boxes
    def __clear_box(self):
        self.__student_ID_entry.delete(0, END)
        self.__first_entry.delete(0, END)
        self.__last_entry.delete(0, END)
        self.__year_entry.delete(0, END)
        self.__course_name_entry.delete(0, END)
        self.__course_ID_entry.delete(0, END)
        self.__professor_entry.delete(0, END)

    # Check that the entered data is valid
    def __check_data_valid(self, requested_sID, requested_values, database_data):

        # Tests if the Student ID is set
        if not requested_sID:
            self.__displayed_data.set(ERROR_ID_EMPTY)
            return

        # Tests if the Student ID is found in the database
        # Note that this is disabled if set to False,
        # since add_data does not want this behavior
        if database_data is not False and not database_data:
            self.__displayed_data.set(ERROR_ID_NOT_FOUND)
            return False

        # Variables for readability
        requested_year = requested_values[3]
        requested_cID = requested_values[5]

        # Tests if Student ID is numeric
        if not requested_sID.isdigit():
            self.__displayed_data.set(ERROR_ID_NOT_INT)
            return False

        # Tests if Student ID is 5 characters long
        if len(requested_sID) != 5:
            self.__displayed_data.set(ERROR_ID_WRONG_LENGTH)
            return False

        # Tests if the year is numeric or not specified
        if requested_year and not requested_year.isdigit():
            self.__displayed_data.set(ERROR_SCHOOL_YEAR_NOT_INT)
            return False

        # Tests if the course ID is numeric or not specified
        if requested_cID and not requested_cID.isdigit():
            self.__displayed_data.set(ERROR_COURSE_ID_NOT_INT)
            return False

        # All tests passed by this point
        return True


if __name__ == '__main__':
    # Call main and start database
    main()
    student_gui = StudentDatabaseGUI()
