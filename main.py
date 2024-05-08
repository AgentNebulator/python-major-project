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
    data_table = display_select_results(results)

    return data_table


# Create Class for GUI
class StudentDatabase:
    # Use variable data_table from main() to show table
    def __init__(self, data_table):
        # Initiate main window, frames, and labels
        self.main_window = tkinter.Tk()
        self.main_window.title("Database")
        self.top_frame = tkinter.Frame(self.main_window)
        self.mid_frame = tkinter.Frame(self.main_window)
        self.bottom_frame = tkinter.Frame(self.main_window)
        self.value = tkinter.StringVar()

        # Text is variable data_table to display table
        self.data_label = tkinter.Label(self.top_frame,
                                        text=data_table)

        # Exit button for user-friendly exit
        self.exit_button = tkinter.Button(self.mid_frame,
                                          text='Exit',
                                          command=self.main_window.destroy)

        # Pack data
        self.data_label.pack()
        self.exit_button.pack(side='left')

        self.top_frame.pack(padx=(40, 40), pady=(40, 10))
        self.mid_frame.pack(padx=(40, 40), pady=(10, 10))
        self.bottom_frame.pack(padx=(40, 40), pady=(10, 40))
        tkinter.mainloop()


def display_select_results(results):
    print(tabulate(results[1], headers=results[0], tablefmt="rounded_outline", numalign="left"))


# Call both functions
student_gui = StudentDatabase(main())


if __name__ == '__main__':
    main()
