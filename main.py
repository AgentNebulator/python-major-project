# Week 13: program 1 (Team)
# Code by __________ (MM/DD/2024)

import sqlite3
from tabulate import tabulate

def main():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    #I emailed the professor about what we should put down. Might have to look at next week to see what data we are dealing with
    cur.execute('''CREATE TABLE Database (student_name_last TEXT, student_name_first TEXT, student_id INTEGER, sutdent_year INTEGER, course_name TEXT, course_ID INTEGER, professor_name TEXT)''')

    cur.execute('INSERT INTO Database VALUES ("Smith", "Ethan", 2048, 11, "Python", "2005", "McAnally")')
    
    # Select the data and extract results
    cur.execute('SELECT * FROM Database')
    headers = [desc[0] for desc in cur.description] # headers are the column headers
    data = cur.fetchall() # data is the data in the table, excluding headers
    
    # Close the connection
    conn.close()
    
    # Put the results together as a tuple
    results = (headers, data)
    display_select_results(results)
    
def display_select_results(results):
    # Use the tabulate package to print results
    # Try using tablefmt="grid" and playing around with other parameters found online
    print(tabulate(results[1], headers=results[0], tablefmt="fancy_outline", numalign="left"))

if __name__ == '__main__':
    main()
