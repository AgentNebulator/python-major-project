# Week 14: Second program (Major Project Part 2)
# Code by team of Mathias Laven, Ethan Smith, Kathleen Brozynski (05/07/2024)

import sqlite3
from tabulate import tabulate
import student_data
import tkinter
import tkinter.ttk

DISPLAYED_DATA_DEFAULT = "Use Student ID to request specific data"
DISPLAYED_DATA_ERROR = "No student found with that ID"

TABLE_COLUMN_WIDTH = 100


def main():
    conn = sqlite3.connect('student_database.db')
    cur = conn.cursor()

    # Create table
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS Students (student_id INTEGER PRIMARY KEY NOT NULL, last_name TEXT, 
        first_name TEXT, school_year INTEGER, course_name TEXT, course_ID INTEGER, professor_name TEXT)'''
    )

    # Enter data
    cur.executemany('INSERT OR IGNORE INTO Students VALUES (?, ?, ?, ?, ?, ?, ?)', student_data.data)

    # Close the connection
    conn.commit()
    conn.close()


# Create Class for GUI
class StudentDatabaseGUI:
    # Use variable data_table from main() to show table
    def __init__(self):
        conn = sqlite3.connect('student_database.db')
        cur = conn.cursor()

        # Select the data and extract results
        cur.execute('SELECT * FROM Students')
        headers = [desc[0] for desc in cur.description]  # headers are the column headers
        data = cur.fetchall()  # data is the data in the table, excluding headers

        # Put the results together as a tuple and store
        self.__data = (headers, data)

        # Close connection
        conn.close()

        # Initiate main window, frames, and labels
        self.__main_window = tkinter.Tk()
        self.__main_window.title("Database")

        # Create frames
        self.__treeview_frame = tkinter.Frame(self.__main_window)
        self.__label_frame = tkinter.Frame(self.__main_window)
        self.__entry_frame = tkinter.Frame(self.__main_window)
        self.__button_frame = tkinter.Frame(self.__main_window)

        # Create data table (well, treeview)
        # Treeview information sourced from https://pythonguides.com/python-tkinter-table-tutorial/
        self.__data_table = tkinter.ttk.Treeview(self.__treeview_frame)

        # Set the headers to the data headers
        self.__data_table['columns'] = self.__data[0]

        # Set the default columns and headings to not show
        self.__data_table.column("#0", width=0, stretch=False)
        self.__data_table.heading("#0", anchor="center")

        # Format columns and headings
        for header in self.__data[0]:
            self.__data_table.column(header, anchor="center", width=TABLE_COLUMN_WIDTH)
            self.__data_table.heading(header, text=header, anchor="center")

        # Insert data
        for student in self.__data[1]:
            self.__data_table.insert(parent='', index='end', values=student)

        # Create label text for special requested data
        self.__displayed_data = tkinter.StringVar()
        self.__displayed_data.set(DISPLAYED_DATA_DEFAULT)

        # Create label and format with text
        self.__data_label = tkinter.Label(self.__label_frame,
                                          textvariable=self.__displayed_data, )

        # Create label and entry box for student ID
        self.__request_label = tkinter.Label(self.__entry_frame, text="Student ID: ")
        self.__request_entry = tkinter.Entry(self.__entry_frame)

        # Create button to delete data by ID
        self.__delete_button = tkinter.Button(self.__button_frame,
                                              text='Delete',
                                              command=self.__delete_data)

        # Create exit button for user-friendly exit
        self.__exit_button = tkinter.Button(self.__button_frame,
                                            text='Exit',
                                            command=self.__main_window.destroy)

        # Pack elements
        self.__data_table.pack()

        self.__data_label.pack(ipadx=10, ipady=10)

        self.__request_label.pack(side="left")
        self.__request_entry.pack()

        self.__delete_button.pack(side="left")
        self.__exit_button.pack(side='left')

        self.__treeview_frame.pack(padx=(10, 10), pady=(10, 10))
        self.__label_frame.pack(padx=(40, 40), pady=(10, 10))
        self.__entry_frame.pack(padx=(40, 40), pady=(10, 10))
        self.__button_frame.pack(padx=(40, 40), pady=(10, 40))

        # Main loop
        tkinter.mainloop()

    def __delete_data(self):
        # Connect to database
        conn = sqlite3.connect('student_database.db')
        cur = conn.cursor()
        # Get the input from the entry box
        requested_id = self.__request_entry.get()
        # Use that input to find the row in the database
        cur.execute('''SELECT student_id From Students
                     WHERE student_id == ?''', (requested_id,))
        results = cur.fetchone()

        # If it finds the data, delete it
        if results:
            cur.execute('''DELETE FROM Students
                                WHERE student_id == ?''',
                        (requested_id,))

            conn.commit()
            # Changes displayed_data text
            self.__displayed_data.set('The student was deleted.')
            # Call update_treeview to update GUI
            self.__update_treeview()
        # If not, displays that there is no data that matches
        else:
            # If no student with provided ID, error
            self.__displayed_data.set(DISPLAYED_DATA_ERROR)

        conn.close()

    def __update_treeview(self):
        # Clear the existing data in the treeview
        for item in self.__data_table.get_children():
            self.__data_table.delete(item)

        # Re-fetch and re-insert the data from the database
        conn = sqlite3.connect('student_database.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM Students')
        data = cur.fetchall()

        for student in data:
            self.__data_table.insert(parent='', index='end', values=student)

        conn.close()


def display_select_results(results):
    # No longer called, but kept just in case
    formatted_results = tabulate(results[1], headers=results[0], tablefmt="rounded_outline", numalign="left")
    print(formatted_results)


if __name__ == '__main__':
    # Call both functions
    main()
    student_gui = StudentDatabaseGUI()
