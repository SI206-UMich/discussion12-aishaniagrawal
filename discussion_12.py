import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
# starter code

# Create Database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


# TASK 1
# CREATE TABLE FOR EMPLOYEE INFORMATION IN DATABASE AND ADD INFORMATION
def create_employee_table(cur, conn):
    cur.execute('drop table if exists employees')
    cur.execute('create table if not exists employees (employee_id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, job_id INTEGER, hire_date DATE, salary NUMBER)')
    conn.commit()

# ADD EMPLOYEE'S INFORMTION TO THE TABLE

def add_employee(filename, cur, conn):
    #load .json file and read job data
    # WE GAVE YOU THIS TO READ IN DATA
    f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), filename)))
    file_data = f.read()
    f.close()
    # THE REST IS UP TO YOU
    data = json.loads(file_data)
    for item in data:
        emp_id = item['employee_id']
        f_name = item['first_name']
        l_name = item['last_name']
        hire_date = item['hire_date']
        job_id = item['job_id']
        salary = item['salary']

        cur.execute('insert or ignore into employees (employee_id, first_name, last_name, job_id, hire_date, salary) values (?,?,?,?,?,?)', (emp_id, f_name, l_name, job_id, hire_date, salary))
        conn.commit()

# TASK 2: GET JOB AND HIRE_DATE INFORMATION
def job_and_hire_date(cur, conn):
    cur.execute('SELECT jobs.job_title, employees.hire_date FROM jobs JOIN employees ON jobs.job_id = employees.job_id ORDER BY employees.hire_date LIMIT 1')
    x = cur.fetchone()
    return x[0]

# TASK 3: IDENTIFY PROBLEMATIC SALARY DATA
# Apply JOIN clause to match individual employees
def problematic_salary(cur, conn):
    cur.execute('select employees.first_name, employees.last_name from employees join jobs on jobs.job_id = employees.job_id where employees.salary < jobs.min_salary or employees.salary > jobs.max_salary')
    x = cur.fetchall()
    return x

# TASK 4: VISUALIZATION
def visualization_salary_data(cur, conn):
    plt.figure()

    cur.execute(
        '''
        SELECT jobs.job_title, employees.salary
        FROM employees 
        JOIN jobs ON jobs.job_id = employees.job_id
        '''
    )
    res = cur.fetchall()
    conn.commit()
    x,y = zip(*res)
    plt.scatter(x,y)

    cur.execute(
        '''
        select jobs.job_title, jobs.min_salary
        from jobs
        '''
    )
    res = cur.fetchall()
    conn.commit()
    x,y = zip(*res)
    plt.scatter(x,y,color = 'red', marker = 'x')

    cur.execute(
        '''
        select jobs.job_title, jobs.max_salary
        from jobs
        '''
    )
    res = cur.fetchall()
    conn.commit()
    x,y = zip(*res)
    plt.scatter(x,y,color = 'red', marker = 'x')

    plt.xticks(rotation = 45)
    plt.tight_layout()
    plt.show()

class TestDiscussion12(unittest.TestCase):
    def setUp(self) -> None:
        self.cur, self.conn = setUpDatabase('HR.db')

    def test_create_employee_table(self):
        self.cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='employees'")
        table_check = self.cur.fetchall()[0][0]
        self.assertEqual(table_check, 1, "Error: 'employees' table was not found")
        self.cur.execute("SELECT * FROM employees")
        count = len(self.cur.fetchall())
        self.assertEqual(count, 13)

    def test_job_and_hire_date(self):
        self.assertEqual('President', job_and_hire_date(self.cur, self.conn))

    def test_problematic_salary(self):
        sal_list = problematic_salary(self.cur, self.conn)
        self.assertIsInstance(sal_list, list)
        self.assertEqual(sal_list[0], ('Valli', 'Pataballa'))
        self.assertEqual(len(sal_list), 4)


def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('HR.db')
    create_employee_table(cur, conn)

    add_employee("employee.json",cur, conn)

    job_and_hire_date(cur, conn)

    wrong_salary = (problematic_salary(cur, conn))
    print(wrong_salary)

if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)

