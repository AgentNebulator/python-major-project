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
                                          textvariable=self.__displayed_data,
                                          relief="ridge")

        # Create label and entry box for student ID
        self.__request_label = tkinter.Label(self.__entry_frame, text="Student ID: ")
        self.__request_entry = tkinter.Entry(self.__entry_frame)

        # Create button to fetch data by ID
        self.__fetch_button = tkinter.Button(self.__button_frame,
                                             text='Fetch',
                                             command=self.__fetch_data)

        # Create exit button for user-friendly exit
        self.__exit_button = tkinter.Button(self.__button_frame,
                                            text='Exit',
                                            command=self.__main_window.destroy)

        # Pack elements
        self.__data_table.pack()

        self.__data_label.pack(ipadx=10, ipady=10)

        self.__request_label.pack(side="left")
        self.__request_entry.pack()

        self.__fetch_button.pack(side="left", padx="10")
        self.__exit_button.pack(side='left')

        self.__treeview_frame.pack(padx=(10, 10), pady=(10, 10))
        self.__label_frame.pack(padx=(40, 40), pady=(10, 10))
        self.__entry_frame.pack(padx=(40, 40), pady=(10, 10))
        self.__button_frame.pack(padx=(40, 40), pady=(10, 40))

        # Main loop
        tkinter.mainloop()

    def __fetch_data(self):

        # Get an array containing only the data matching the provided ID
        requested_id = self.__request_entry.get()
        requested_data = [item for item in self.__data[1]
                          if (str(item[0]) == requested_id)]

        # If data found matching the ID:
        if requested_data:
            # Format into dictionary for readable text display
            data_dict = {
                "id": requested_data[0][0],
                "last_name": requested_data[0][1],
                "first_name": requested_data[0][2],
                "grade_level": requested_data[0][3],
                "class_name": requested_data[0][4],
                "class_id": requested_data[0][5],
                "class_teacher": requested_data[0][6]
            }

            # Set up text display
            self.__displayed_data.set((
                f"Full Name: {data_dict["first_name"]} {data_dict["last_name"]} \n"
                f"Grade level: {data_dict["grade_level"]} \n"
                f"Class: {data_dict["class_teacher"]}'s {data_dict["class_name"]} {data_dict["class_id"]}"
            ))
        else:
            # If no student with provided ID, error
            self.__displayed_data.set(DISPLAYED_DATA_ERROR)


def display_select_results(results):
    # No longer called, but kept just in case
    formatted_results = tabulate(results[1], headers=results[0], tablefmt="rounded_outline", numalign="left")
    print(formatted_results)


if __name__ == '__main__':
    # Call both functions
    main()
    student_gui = StudentDatabaseGUI()
