# Week 14: Second program (Major Project Part 2)
# Code by team of Mathias Laven, Ethan Smith, Kathleen Brozynski (05/06/2024)

import sqlite3
from tabulate import tabulate


def main():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    # Create table
    cur.execute(
        '''CREATE TABLE Database (student_id INTEGER PRIMARY KEY NOT NULL, student_name_last TEXT, 
        student_name_first TEXT, student_year INTEGER, course_name TEXT, course_ID INTEGER, professor_name TEXT)'''
    )

    # Enter data
    cur.execute('INSERT INTO Database VALUES (2048, "Smith", "Ethan", 11, "Python", "2005", "McAnally")')
    cur.execute('INSERT INTO Database VALUES (1105, "Laven", "Mathias", 11, "Python", "2005", "McAnally")')
    cur.execute('INSERT INTO Database VALUES (1818, "Brozynski", "Kathleen", 11, "Python", "2005", "McAnally")')
    cur.execute('INSERT INTO Database VALUES (1684, "Burgoss", "Rob", 10, "English", "1182", "Johnson")')
    cur.execute('INSERT INTO Database VALUES (2598, "Jacobson", "Paul", 12, "Calculus", "2036", "Schmidt")')
    cur.execute('INSERT INTO Database VALUES (9046, "Smith", "Terry", 11, "Chemistry", "1520", "Nylund")')
    cur.execute('INSERT INTO Database VALUES (7245, "Jackson", "Mary", 12, "French", "1905", "Ramsey")')
    cur.execute('INSERT INTO Database VALUES (9241, "Olson", "Amanda", 11, "Economics", "3060", "Swanson")')
    cur.execute('INSERT INTO Database VALUES (4470, "Miller", "Nathanial", 11, "French", "4009", "Jackson")')
    cur.execute('INSERT INTO Database VALUES (9801, "Blake", "Johnathan", 12, "Calculus", "1000", "Roosevelt")')

    # Select the data and extract results
    cur.execute('SELECT * FROM Database')
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
