# Week 14: Second program (Major Project Part 2)
# Code by team of Mathias Laven, Ethan Smith, Kathleen Brozynski (05/06/2024)

import sqlite3
from tabulate import tabulate
import student_data


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
    display_select_results(results)


def display_select_results(results):
    print(tabulate(results[1], headers=results[0], tablefmt="rounded_outline", numalign="left"))


if __name__ == '__main__':
    main()
