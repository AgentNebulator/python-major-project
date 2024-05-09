# Week 14: Second program (Major Project Part 2)
# Code by team of Mathias Laven, Ethan Smith, Kathleen Brozynski (05/07/2024)

import sqlite3
from tabulate import tabulate
import student_data
import tkinter


def main():
    conn = sqlite3.connect('student_database.db')
    cur = conn.cursor()

    # Create table
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS Students (student_id INTEGER PRIMARY KEY NOT NULL, student_name_last TEXT, 
        student_name_first TEXT, student_year INTEGER, course_name TEXT, course_ID INTEGER, professor_name TEXT)'''
    )

    # Enter data
    cur.executemany('INSERT OR IGNORE INTO Students VALUES (?, ?, ?, ?, ?, ?, ?)', student_data.data)

    # Select the data and extract results
    cur.execute('SELECT * FROM Students')
    headers = [desc[0] for desc in cur.description]  # headers are the column headers
    data = cur.fetchall()  # data is the data in the table, excluding headers

    # Close the connection
    conn.commit()
    conn.close()

    # Put the results together as a tuple
    results = (headers, data)

    return results


# Create Class for GUI
class StudentDatabaseGUI:
    # Use variable data_table from main() to show table
    def __init__(self, results):

        self.__data = results
        self.__data_table = display_select_results(results)

        # Initiate main window, frames, and labels
        self.__main_window = tkinter.Tk()
        self.__main_window.title("Database")
        self.__top_frame = tkinter.Frame(self.__main_window)
        self.__mid_frame = tkinter.Frame(self.__main_window)
        self.__bottom_frame = tkinter.Frame(self.__main_window)
        self.__value = tkinter.StringVar()

        # Text is variable data_table to display table
        self.__data_label = tkinter.Label(self.__top_frame,
                                        text=self.__data_table)

        self.__request_entry = tkinter.Entry(self.__mid_frame)

        # Exit button for user-friendly exit
        self.__exit_button = tkinter.Button(self.__bottom_frame,
                                          text='Exit',
                                          command=self.__close_window)

        # Pack data
        self.__data_label.pack()
        self.__request_entry.pack()
        self.__exit_button.pack(side='left')

        self.__top_frame.pack(padx=(40, 40), pady=(40, 10))
        self.__mid_frame.pack(padx=(40, 40), pady=(10, 10))
        self.__bottom_frame.pack(padx=(40, 40), pady=(10, 40))

        tkinter.mainloop()

    def __close_window(self):
        # was experimenting and left this in
        # unnecessary right now, but could possibly be useful in the future
        self.__main_window.destroy()


def display_select_results(results):
    formatted_results = tabulate(results[1], headers=results[0], tablefmt="rounded_outline", numalign="left")
    print(formatted_results)

    return formatted_results


if __name__ == '__main__':
    # Call both functions
    student_gui = StudentDatabaseGUI(main())


