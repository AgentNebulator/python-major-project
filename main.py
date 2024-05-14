# Week 15: Final Project
# Code by team of Mathias Laven, Ethan Smith, Kathleen Brozynski (05/15/2024)

import sqlite3
from tabulate import tabulate
import student_data
import tkinter
import tkinter.ttk
from tkinter import END

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
        self.__student_ID_label = tkinter.Label(self.__entry_frame, text="Student ID: ")
        self.__student_ID_entry = tkinter.Entry(self.__entry_frame)

        self.__last_label = tkinter.Label(self.__entry_frame, text="Last Name: ")
        self.__last_entry = tkinter.Entry(self.__entry_frame)

        self.__first_label = tkinter.Label(self.__entry_frame, text="First Name: ")
        self.__first_entry = tkinter.Entry(self.__entry_frame)

        self.__year_label = tkinter.Label(self.__entry_frame, text="School Year: ")
        self.__year_entry = tkinter.Entry(self.__entry_frame, width=10)

        self.__course_name_label = tkinter.Label(self.__entry_frame, text="Course Name: ")
        self.__course_name_entry = tkinter.Entry(self.__entry_frame)

        self.__course_ID_label = tkinter.Label(self.__entry_frame, text="Course ID: ")
        self.__course_ID_entry = tkinter.Entry(self.__entry_frame)

        self.__professor_label = tkinter.Label(self.__entry_frame, text="Professor Name: ")
        self.__professor_entry = tkinter.Entry(self.__entry_frame)

        # Create button to delete data by ID
        self.__delete_button = tkinter.Button(self.__button_frame,
                                              text='Delete',
                                              command=self.__delete_data)
        # Create button to add data
        self.__add_button = tkinter.Button(self.__button_frame,
                                             text='Add Data',
                                             command=self.__add_data)

        # Create exit button for user-friendly exit
        self.__exit_button = tkinter.Button(self.__button_frame,
                                            text='Exit',
                                            command=self.__main_window.destroy)

        # Pack elements
        self.__data_table.pack()

        self.__data_label.pack(ipadx=10, ipady=10)

        self.__student_ID_label.pack(side="left")
        self.__student_ID_entry.pack(side="left")

        self.__last_label.pack(side="left")
        self.__last_entry.pack(side="left")

        self.__first_label.pack(side="left")
        self.__first_entry.pack(side="left")

        self.__year_label.pack(side="left")
        self.__year_entry.pack(side="left")

        self.__course_name_label.pack(side="left")
        self.__course_name_entry.pack(side="left")

        self.__course_ID_label.pack(side="left")
        self.__course_ID_entry.pack(side="left")

        self.__professor_label.pack(side="left")
        self.__professor_entry.pack(side="left")

        self.__delete_button.pack(side="left")
        self.__add_button.pack(side="left", padx="10")
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
        # Get the input from the entry box
        cur = conn.cursor()
        # Use that input to find the row in the database
        requested_id = self.__student_ID_entry.get()

        # If it finds the data, delete it
        cur.execute('''SELECT student_id From Students
                     WHERE student_id == ?''', (requested_id,))
        results = cur.fetchone()
    
        if results != None:
            cur.execute('''DELETE FROM Students
                                WHERE student_id == ?''',
                                (requested_id,))
            
            conn.commit()
            self.__displayed_data.set('The student was deleted.')
            # Call update_treeview to update GUI
            self.__update_treeview()
            
        # If not, display "No student found with that ID"
        else:
            # If no student with provided ID, error
            self.__displayed_data.set(DISPLAYED_DATA_ERROR)

        self.__clear_box()
        conn.close()

    def __add_data(self):
        # Connect to database
        conn = sqlite3.connect('student_database.db')
        cur = conn.cursor()

        # Get users input in the GUI
        requested_sid = self.__student_ID_entry.get()
        requested_last = self.__last_entry.get()
        requested_first = self.__first_entry.get()
        requested_year = self.__year_entry.get()
        requested_cname = self.__course_name_entry.get()
        requested_cID = self.__course_ID_entry.get()
        requested_professor = self.__professor_entry.get()

        # Add row with those values
        cur.execute('''INSERT INTO Students (student_id, last_name, first_name, school_year, course_name, course_ID, professor_name)
                    VALUES (?,?,?,?,?,?,?) ''', 
                    (requested_sid, requested_last, requested_first, requested_year, requested_cname, requested_cID, requested_professor))
        
        conn.commit()

        self.__displayed_data.set('The student was added.')

        # Update GUI table
        self.__update_treeview()
        self.__clear_box()
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

    # Clear all entries boxes
    def __clear_box(self):
        self.__student_ID_entry.delete(0, END)
        self.__first_entry.delete(0,END)
        self.__last_entry.delete(0,END)
        self.__year_entry.delete(0,END)
        self.__course_name_entry.delete(0,END)
        self.__course_ID_entry.delete(0,END)
        self.__professor_entry.delete(0,END)

if __name__ == '__main__':
    # Call both functions
    main()
    student_gui = StudentDatabaseGUI()
