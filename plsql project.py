import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk
conn = sqlite3.connect('library.db')
cursor = conn.cursor()
def create_tables():  
    cursor.execute('''CREATE TABLE IF NOT EXISTS Books (
                        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT, 
                        author TEXT, 
                        publisher TEXT, 
                        published_date DATE, 
                        quantity INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Members (
                        member_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        name TEXT, 
                        email TEXT, 
                        phone_number TEXT, 
                        membership_date DATE)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Borrow (
                        borrow_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        member_id INTEGER, 
                        book_id INTEGER, 
                        issue_date DATE, 
                        return_date DATE, 
                        FOREIGN KEY(member_id) REFERENCES Members(member_id),
                        FOREIGN KEY(book_id) REFERENCES Books(book_id))''')
    conn.commit()
def add_book(title, author, publisher, published_date, quantity):
    try:
        cursor.execute('''INSERT INTO Books (title, author, publisher, published_date, quantity)
                          VALUES (?, ?, ?, ?, ?)''', (title, author, publisher, published_date, quantity))
        conn.commit()
        messagebox.showinfo("Success", "Book added successfully.")
        display_books()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add book: {e}")
def register_member(name, email, phone_number):
    try:
        cursor.execute('''INSERT INTO Members (name, email, phone_number, membership_date)
                          VALUES (?, ?, ?, ?)''', (name, email, phone_number, datetime.now()))
        conn.commit()
        messagebox.showinfo("Success", "Member registered successfully.")
        display_members()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to register member: {e}")
def delete_book(book_id):
    try:
        cursor.execute('DELETE FROM Books WHERE book_id = ?', (book_id,))
        conn.commit()
        messagebox.showinfo("Success", "Book deleted successfully.")
        display_books()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete book: {e}")
def delete_member(member_id):
    try:
        cursor.execute('DELETE FROM Members WHERE member_id = ?', (member_id,))
        conn.commit()
        messagebox.showinfo("Success", "Member deleted successfully.")
        display_members()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete member: {e}")
def issue_book(member_id, book_id):
    try:
        cursor.execute("SELECT quantity FROM Books WHERE book_id = ?", (book_id,))
        quantity = cursor.fetchone()
        if quantity and quantity[0] > 0:
            cursor.execute('''INSERT INTO Borrow (member_id, book_id, issue_date)
                              VALUES (?, ?, ?)''', (member_id, book_id, datetime.now()))
            cursor.execute('''UPDATE Books SET quantity = quantity - 1 WHERE book_id = ?''', (book_id,))
            conn.commit()
            messagebox.showinfo("Success", "Book issued successfully.")
        else:
            messagebox.showwarning("Unavailable", "Book not available.")
        display_books()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to issue book: {e}")
def return_book(member_id, book_id):
    try:
        cursor.execute('''UPDATE Borrow SET return_date = ? 
                          WHERE member_id = ? AND book_id = ? AND return_date IS NULL''', 
                       (datetime.now(), member_id, book_id))
        cursor.execute('''UPDATE Books SET quantity = quantity + 1 WHERE book_id = ?''', (book_id,))
        conn.commit()
        messagebox.showinfo("Success", "Book returned successfully.")
        display_books()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to return book: {e}")
def display_books():
    cursor.execute("SELECT * FROM Books")
    books = cursor.fetchall()
    display_text = "\nBooks Available in the Library:\n"
    for book in books:
        display_text += f"Book ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Publisher: {book[3]}, Published Date: {book[4]}, Quantity: {book[5]}\n"
    result_text.delete(1.0, tk.END)  # Clear previous text
    result_text.insert(tk.END, display_text)
def display_members():
    cursor.execute("SELECT * FROM Members")
    members = cursor.fetchall()
    display_text = "\nRegistered Members:\n"
    for member in members:
        display_text += f"Member ID: {member[0]}, Name: {member[1]}, Email: {member[2]}, Phone: {member[3]}, Membership Date: {member[4]}\n"
    result_text.delete(1.0, tk.END)  # Clear previous text
    result_text.insert(tk.END, display_text)
def display_borrow_history():
    cursor.execute("SELECT * FROM Borrow")
    borrow_history = cursor.fetchall()
    display_text = "\nBorrow History:\n"
    for record in borrow_history:
        display_text += f"Borrow ID: {record[0]}, Member ID: {record[1]}, Book ID: {record[2]}, Issue Date: {record[3]}, Return Date: {record[4]}\n"
    result_text.delete(1.0, tk.END)  # Clear previous text
    result_text.insert(tk.END, display_text)
root = tk.Tk()
root.title("Library Management System")
root.geometry("800x600")
root.configure(bg="#ffffff")
style = ttk.Style()
style.configure("TButton", font=("Arial", 10, "bold"), padding=8)
style.configure("TLabel", font=("Arial", 10), background="#e6f2ff")
style.configure("TFrame", background="#f0f0f5")
style.configure("TEntry", padding=5)
header = tk.Label(root, text="Library Management System", font=("Arial", 24, "bold"), fg="#333333", bg="#e6f2ff")
header.pack(pady=10)
main_frame = ttk.Frame(root, padding=20, style="TFrame")
main_frame.pack(expand=True, fill="both")
book_frame = ttk.Frame(main_frame, style="TFrame")
book_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
member_frame = ttk.Frame(main_frame, style="TFrame")
member_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
action_frame = ttk.Frame(main_frame, style="TFrame")
action_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="nsew")
main_frame.rowconfigure(0, weight=1)
main_frame.columnconfigure([0, 1], weight=1)
ttk.Label(book_frame, text="Add New Book", font=("Arial", 14, "bold"), background="#e6f2ff").grid(row=0, column=0, columnspan=2, pady=5)
labels = ["Title", "Author", "Publisher", "Published Date (YYYY-MM-DD)", "Quantity"]
entries = []
for idx, label in enumerate(labels):
    ttk.Label(book_frame, text=label).grid(row=idx + 1, column=0, sticky="w", pady=5)
    entry = ttk.Entry(book_frame, width=30)
    entry.grid(row=idx + 1, column=1, padx=5)
    entries.append(entry)
ttk.Button(book_frame, text="Add Book", command=lambda: add_book(*[e.get() for e in entries])).grid(row=6, column=0, columnspan=2, pady=10)
ttk.Label(member_frame, text="Register Member", font=("Arial", 14, "bold"), background="#e6f2ff").grid(row=0, column=0, columnspan=2, pady=5)
member_labels = ["Member Name", "Email", "Phone Number"]
member_entries = []
for idx, label in enumerate(member_labels):
    ttk.Label(member_frame, text=label).grid(row=idx + 1, column=0, sticky="w", pady=5)
    entry = ttk.Entry(member_frame, width=30)
    entry.grid(row=idx + 1, column=1, padx=5)
    member_entries.append(entry)
ttk.Button(member_frame, text="Register Member", command=lambda: register_member(*[e.get() for e in member_entries])).grid(row=4, column=0, columnspan=2, pady=10)
ttk.Label(action_frame, text="Issue/Return Book", font=("Arial", 14, "bold"), background="#e6f2ff").grid(row=0, column=0, columnspan=2, pady=5)
ttk.Label(action_frame, text="Member ID").grid(row=1, column=0, sticky="w", pady=5)
member_id_entry = ttk.Entry(action_frame, width=10)
member_id_entry.grid(row=1, column=1)
ttk.Label(action_frame, text="Book ID").grid(row=2, column=0, sticky="w", pady=5)
book_id_entry = ttk.Entry(action_frame, width=10)
book_id_entry.grid(row=2, column=1)
ttk.Button(action_frame, text="Issue Book", command=lambda: issue_book(int(member_id_entry.get()), int(book_id_entry.get()))).grid(row=3, column=0, columnspan=2, pady=5)
ttk.Button(action_frame, text="Return Book", command=lambda: return_book(int(member_id_entry.get()), int(book_id_entry.get()))).grid(row=4, column=0, columnspan=2, pady=5)
ttk.Label(action_frame, text="Delete Book", font=("Arial", 10, "bold"), background="#e6f2ff").grid(row=5, column=0, columnspan=2, pady=5)
delete_book_id_entry = ttk.Entry(action_frame, width=10)
delete_book_id_entry.grid(row=6, column=0)
ttk.Button(action_frame, text="Delete Book", command=lambda: delete_book(int(delete_book_id_entry.get()))).grid(row=6, column=1)
ttk.Label(action_frame, text="Delete Member", font=("Arial", 10, "bold"), background="#e6f2ff").grid(row=7, column=0, columnspan=2, pady=5)
delete_member_id_entry = ttk.Entry(action_frame, width=10)
delete_member_id_entry.grid(row=8, column=0)
ttk.Button(action_frame, text="Delete Member", command=lambda: delete_member(int(delete_member_id_entry.get()))).grid(row=8, column=1)
ttk.Button(main_frame, text="View All Books", command=display_books).grid(row=2, column=0, pady=10)
ttk.Button(main_frame, text="View All Members", command=display_members).grid(row=2, column=1, pady=10)
ttk.Button(main_frame, text="View Borrow History", command=display_borrow_history).grid(row=3, column=0, columnspan=2, pady=10)
result_text = tk.Text(root, height=10, width=80, wrap="word", font=("Arial", 10))
result_text.pack(pady=10, padx=20)
result_text.config(state=tk.NORMAL)
create_tables()
root.mainloop()
