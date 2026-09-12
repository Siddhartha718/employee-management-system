import tkinter as tk
from tkinter import ttk, messagebox
from database import connect_database
import mysql.connector


# Connect to MySQL
connection = connect_database()
cursor = connection.cursor()

# Store selected employee ID
selected_employee_id = None


# Create main window
root = tk.Tk()
root.title("Employee Management System")
root.geometry("800x600")


# Heading
heading = tk.Label(
    root,
    text="EMPLOYEE MANAGEMENT SYSTEM",
    font=("Arial", 20, "bold")
)
heading.pack(pady=20)


# Form frame
form_frame = tk.LabelFrame(
    root,
    text="Employee Information",
    padx=20,
    pady=10
)
form_frame.pack(
    padx=20,
    pady=10
)


# Employee Name
name_label = tk.Label(
    form_frame,
    text="Employee Name:",
    font=("Arial", 12)
)
name_label.grid(
    row=0,
    column=0,
    padx=10,
    pady=8
)

name_entry = tk.Entry(
    form_frame,
    width=40
)
name_entry.grid(
    row=0,
    column=1,
    padx=10,
    pady=8
)


# Department
department_label = tk.Label(
    form_frame,
    text="Department:",
    font=("Arial", 12)
)
department_label.grid(
    row=1,
    column=0,
    padx=10,
    pady=8
)

department_entry = tk.Entry(
    form_frame,
    width=40
)
department_entry.grid(
    row=1,
    column=1,
    padx=10,
    pady=8
)


# Salary
salary_label = tk.Label(
    form_frame,
    text="Salary:",
    font=("Arial", 12)
)
salary_label.grid(
    row=2,
    column=0,
    padx=10,
    pady=8
)

salary_entry = tk.Entry(
    form_frame,
    width=40
)
salary_entry.grid(
    row=2,
    column=1,
    padx=10,
    pady=8
)


# Employee table
employee_table = ttk.Treeview(
    root,
    columns=("ID", "Name", "Department", "Salary"),
    show="headings",
    height=12
)

employee_table.heading(
    "ID",
    text="Employee ID"
)

employee_table.heading(
    "Name",
    text="Employee Name"
)

employee_table.heading(
    "Department",
    text="Department"
)

employee_table.heading(
    "Salary",
    text="Salary"
)

employee_table.column(
    "ID",
    width=60,
    anchor="center"
)

employee_table.column(
    "Name",
    width=220,
    anchor="center"
)

employee_table.column(
    "Department",
    width=180,
    anchor="center"
)

employee_table.column(
    "Salary",
    width=120,
    anchor="center"
)

employee_table.pack(
    padx=20,
    pady=10,
    fill="x"
)


# Load employees from MySQL
def load_employees():

    # Clear existing rows from the table
    for row in employee_table.get_children():
        employee_table.delete(row)

    # Fetch all employees from MySQL
    cursor.execute("SELECT * FROM tblemployee")
    employees = cursor.fetchall()

    # Display employees in the Treeview
    for employee in employees:
        employee_table.insert(
            "",
            tk.END,
            values=employee
        )


# Add employee
def add_employee():

    # Get data from input fields
    name = name_entry.get()
    department = department_entry.get()
    salary = salary_entry.get()

    # Validate empty fields
    if name == "" or department == "" or salary == "":
        messagebox.showwarning(
            "Warning",
            "Please fill all fields!"
        )
        return

    # Validate salary
    if not salary.isdigit():
        messagebox.showerror(
            "Invalid Salary",
            "Salary must be a number!"
        )
        return

    # SQL INSERT query
    query = """
        INSERT INTO tblemployee (empname, department, salary)
        VALUES (%s, %s, %s)
    """

    values = (name, department, salary)

    # Execute query and save changes
    try:
        cursor.execute(query, values)
        connection.commit()

    except mysql.connector.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not add employee:\n{error}"
        )
        return

    # Show success message
    messagebox.showinfo(
        "Success",
        "Employee added successfully!"
    )

    # Clear input fields
    name_entry.delete(0, tk.END)
    department_entry.delete(0, tk.END)
    salary_entry.delete(0, tk.END)

    # Refresh employee table
    load_employees()


# Select employee
def select_employee(event):

    global selected_employee_id

    # Get the selected row from the Treeview
    selected_row = employee_table.focus()

    # Stop if no row is selected
    if not selected_row:
        return

    # Get employee data from the selected row
    employee_data = employee_table.item(selected_row)

    # Get the values from the selected employee
    values = employee_data["values"]

    # Store the selected employee ID
    selected_employee_id = values[0]

    # Clear the Name field
    name_entry.delete(0, tk.END)

    # Insert selected employee name
    name_entry.insert(0, values[1])

    # Clear the Department field
    department_entry.delete(0, tk.END)

    # Insert selected department
    department_entry.insert(0, values[2])

    # Clear the Salary field
    salary_entry.delete(0, tk.END)

    # Insert selected salary
    salary_entry.insert(0, values[3])


# Update employee
def update_employee():

    global selected_employee_id

    # Check whether an employee is selected
    if selected_employee_id is None:
        messagebox.showwarning(
            "Warning",
            "Please select an employee first!"
        )
        return

    # Get updated employee data from input fields
    name = name_entry.get()
    department = department_entry.get()
    salary = salary_entry.get()

    # Validate empty fields
    if name == "" or department == "" or salary == "":
        messagebox.showwarning(
            "Warning",
            "Please fill all fields!"
        )
        return

    # Validate salary
    if not salary.isdigit():
        messagebox.showerror(
            "Invalid Salary",
            "Salary must be a number!"
        )
        return

    # SQL UPDATE query
    query = """
        UPDATE tblemployee
        SET empname = %s,
            department = %s,
            salary = %s
        WHERE empid = %s
    """

    # Values for the UPDATE query
    values = (
        name,
        department,
        salary,
        selected_employee_id
    )

    # Execute UPDATE query and save changes
    try:
        cursor.execute(query, values)
        connection.commit()

    except mysql.connector.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not update employee:\n{error}"
        )
        return

    # Show success message
    messagebox.showinfo(
        "Success",
        "Employee updated successfully!"
    )

    # Refresh the employee table
    load_employees()

    # Clear input fields
    name_entry.delete(0, tk.END)
    department_entry.delete(0, tk.END)
    salary_entry.delete(0, tk.END)

    # Reset selected employee
    selected_employee_id = None


# Delete employee
def delete_employee():

    global selected_employee_id

    # Check whether an employee is selected
    if selected_employee_id is None:
        messagebox.showwarning(
            "Warning",
            "Please select an employee first!"
        )
        return

    # Ask the user for delete confirmation
    answer = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this employee?"
    )

    # Stop if the user cancels deletion
    if not answer:
        return

    # SQL DELETE query
    query = """
        DELETE FROM tblemployee
        WHERE empid = %s
    """

    # Employee ID to be deleted
    values = (
        selected_employee_id,
    )

    # Execute DELETE query and save changes
    try:
        cursor.execute(query, values)
        connection.commit()

    except mysql.connector.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not delete employee:\n{error}"
        )
        return

    # Show success message
    messagebox.showinfo(
        "Success",
        "Employee deleted successfully!"
    )

    # Refresh the employee table
    load_employees()

    # Clear input fields
    name_entry.delete(0, tk.END)
    department_entry.delete(0, tk.END)
    salary_entry.delete(0, tk.END)

    # Reset selected employee
    selected_employee_id = None


# Clear input fields
def clear_fields():

    global selected_employee_id

    # Clear the Name field
    name_entry.delete(0, tk.END)

    # Clear the Department field
    department_entry.delete(0, tk.END)

    # Clear the Salary field
    salary_entry.delete(0, tk.END)

    # Reset selected employee
    selected_employee_id = None


# Button frame
button_frame = tk.Frame(root)
button_frame.pack(pady=10)


# Add Employee button
add_button = tk.Button(
    button_frame,
    text="Add Employee",
    width=15,
    command=add_employee
)
add_button.grid(
    row=0,
    column=0,
    padx=5
)


# View Employees button
view_button = tk.Button(
    button_frame,
    text="View Employees",
    width=15,
    command=load_employees
)
view_button.grid(
    row=0,
    column=1,
    padx=5
)


# Update button
update_button = tk.Button(
    button_frame,
    text="Update",
    width=15,
    command=update_employee
)
update_button.grid(
    row=0,
    column=2,
    padx=5
)


# Delete button
delete_button = tk.Button(
    button_frame,
    text="Delete",
    width=15,
    command=delete_employee
)
delete_button.grid(
    row=0,
    column=3,
    padx=5
)


# Clear button
clear_button = tk.Button(
    button_frame,
    text="Clear",
    width=15,
    command=clear_fields
)
clear_button.grid(
    row=0,
    column=4,
    padx=5
)


# Detect employee selection
employee_table.bind(
    "<ButtonRelease-1>",
    select_employee
)


# Load employees when application starts
load_employees()


# Start application
root.mainloop()

# UI update feature