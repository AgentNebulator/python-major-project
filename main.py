# Week X: __________ program
# Code by __________ (MM/DD/2024)

def main():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    #I emailed the professor about what we should put down. Might have to look at next week to see what data we are dealing with
    cur.execute('''CREATE TABLE Database (student_name NULL, student_id NULL,  course_name NULL, course_ID NULL, na NULL, na2 NULL, na3 NULL)''')
    
    for x in range(10):
        cur.execute('INSERT INTO Database (?,?,?,?,?,?,?)')
        
    conn.commit()
    
    for row in cur.execute("SELECT * FROM Population"):
        print(row)

    conn.close()


if __name__ == '__main__':
    main()
