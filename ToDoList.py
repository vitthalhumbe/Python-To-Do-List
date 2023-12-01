from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import sqlite3

def main_window(username):
    def add_todo():
        new_todo = entry_todo.get()
        if new_todo:
            todo_frame = Frame(main_win)
            todo_frame.pack(anchor="w")

            checkbox_var.append(BooleanVar())
            checkbox = Checkbutton(todo_frame, variable=checkbox_var[-1], font="Verdana 12")
            checkbox.pack(side=LEFT)

            todo_label = Label(todo_frame, text=new_todo, font="Verdana 12")
            todo_label.pack(side=LEFT)

            todo_frames.append(todo_frame)  # Store the frame in the list
            entry_todo.delete(0, END)

            # Save the to-do item to the database
            save_todo_to_database(new_todo, username)
        else:
            messagebox.showwarning("Warning", "Please enter a todo item.")

    def delete_todo():
        selected_todos = [i for i, var in enumerate(checkbox_var) if var.get()]
        selected_todos.reverse()  # Reverse the order to delete from the end
        for index in selected_todos:
            if index < len(todo_frames):  # Check if the index is within the range
                todo_frames[index].destroy()  # Destroy the associated frame
                checkbox_var.pop(index)
                todo_frames.pop(index)

                # Delete the to-do item from the database
                delete_todo_from_database(username, index)

    def save_todo_to_database(todo, user):
        try:
            connection = sqlite3.connect("todos.db")
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS todos (user TEXT, todo TEXT)")

            cursor.execute("INSERT INTO todos VALUES (?, ?)", (user, todo))

            connection.commit()
        except Exception as e:
            print(f"Error saving to-do item to the database: {e}")
        finally:
            connection.close()

    def load_todos_from_database(user):
        todos = []
        try:
            connection = sqlite3.connect("todos.db")
            cursor = connection.cursor()

            cursor.execute("SELECT todo FROM todos WHERE user=?", (user,))
            todos = [row[0] for row in cursor.fetchall()]

        except Exception as e:
            print(f"Error loading to-do items from the database: {e}")
        finally:
            connection.close()

        return todos

    def delete_todo_from_database(user, index):
        try:
            connection = sqlite3.connect("todos.db")
            cursor = connection.cursor()

            cursor.execute("SELECT todo FROM todos WHERE user=?", (user,))
            todos = [row[0] for row in cursor.fetchall()]

            if index < len(todos):
                cursor.execute("DELETE FROM todos WHERE user=? AND todo=?", (user, todos[index]))

            connection.commit()
        except Exception as e:
            print(f"Error deleting to-do item from the database: {e}")
        finally:
            connection.close()

    main_win = Tk()
    main_win.title(f'To Do List | Welcome, {username}')
    main_win.geometry("500x500")

    # To-Do List
    label_todos = Label(main_win, text='To-Do List', font="Verdana 14 bold")
    label_todos.pack(pady=10)

    entry_todo = Entry(main_win, width=30, font="Verdana 12")
    entry_todo.pack(pady=10)

    btn_add_todo = Button(main_win, text="Add Todo", width=15, command=add_todo, font="Verdana 10 bold")
    btn_add_todo.pack(pady=5)

    btn_delete_todo = Button(main_win, text="Delete Selected", width=15, command=delete_todo, font="Verdana 10 bold")
    btn_delete_todo.pack(pady=5)

    checkbox_var = []  # List to store BooleanVars for checkboxes
    todo_frames = []  # List to store frames for each to-do item

    # Load existing to-do items from the database
    existing_todos = load_todos_from_database(username)
    for todo in existing_todos:
        todo_frame = Frame(main_win)
        todo_frame.pack(anchor="w")

        checkbox_var.append(BooleanVar())
        checkbox = Checkbutton(todo_frame, variable=checkbox_var[-1], font="Verdana 12")
        checkbox.pack(side=LEFT)

        todo_label = Label(todo_frame, text=todo, font="Verdana 12")
        todo_label.pack(side=LEFT)

        todo_frames.append(todo_frame)  # Store the frame in the list

    main_win.mainloop()


def login():
    def login_action():
        entered_username = username_var.get()
        entered_password = password_var.get()

        try:
            con = mysql.connector.connect(host='localhost', user='root', password='My@vitthal#15', database='users')
            cur = con.cursor()
            cur.execute("SELECT * FROM user_info WHERE username=%s AND user_password=%s", (entered_username, entered_password))
            row = cur.fetchone()

            if row is not None:
                con.close()
                messagebox.showinfo("Success", "Login Successful", parent=winlogin)
                winlogin.destroy()  # Close the login window
                main_window(entered_username)  # Pass the username to the main window
            else:
                messagebox.showerror("Error", "Invalid username or password", parent=winlogin)

        except Exception as es:
            messagebox.showerror("Error", f"Error Due to: {str(es)}", parent=winlogin)

    def open_signup():
        winlogin.destroy()  # Close the login window
        signup()
        
    winlogin = Tk()
    winlogin.title('To Do List | Login')
    winlogin.geometry("500x500")

    # Heading
    heading = Label(winlogin, text='Login', font="Verdana 20 bold")
    heading.place(x=80, y=60)

    # Username
    username_label = Label(winlogin, text='Username:', font="Verdana 10 bold")
    username_label.place(x=80, y=100)
    username_var = StringVar()
    username_entry = Entry(winlogin, width=40, textvariable=username_var)
    username_entry.place(x=220, y=100)

    # Password
    password_label = Label(winlogin, text='Password:', font="Verdana 10 bold")
    password_label.place(x=80, y=130)
    password_var = StringVar()
    password_entry = Entry(winlogin, width=40, show='*', textvariable=password_var)
    password_entry.place(x=220, y=130)

    # Don't have an account link
    signup_link = Label(winlogin, text="Don't have an account? Sign up", font="Verdana 10 underline", fg="blue", cursor="hand2")
    signup_link.place(x=80, y=190)
    signup_link.bind("<Button-1>", lambda e: open_signup())

    # Buttons
    btn_login = Button(winlogin, width=20, text='Login', font="Verdana 10 bold", command=login_action)
    btn_login.place(x=80, y=160)

    winlogin.mainloop()


def signup():
    def action():
        if username_var.get() == '' or password_var.get() == '' or email_var.get() == '' or cr_password_var.get() == '':
            messagebox.showerror("Error", "All Fields are Required", parent=winsignup)
        elif password_var.get() != cr_password_var.get():
            messagebox.showwarning("Warning", 'Password and Confirm password should be the same', parent=winsignup)
        else:
            try:
                con = mysql.connector.connect(host='localhost', user='root', password='My@vitthal#15',
                                              database='users')
                cur = con.cursor()
                cur.execute("SELECT * FROM user_info WHERE username=%s", (username_var.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Username already exists", parent=winsignup)
                else:
                    query = "INSERT INTO user_info (username, user_password, user_email) VALUES (%s, %s, %s)"
                    data = (username_var.get(), password_var.get(), email_var.get())
                    cur.execute(query, data)
                    con.commit()
                    con.close()

                    loading_screen.destroy()  # Destroy loading screen
                    messagebox.showinfo("Success", "Registration Successful", parent=winsignup)

                    # Open the main window after successful signup
                    winsignup.destroy()  # Close the signup window
                    main_window(username_entry.get())

            except Exception as es:
                loading_screen.destroy()  # Destroy loading screen
                messagebox.showerror("Error", f"Error Due to: {str(es)}", parent=winsignup)

    def open_login():
        winsignup.destroy()  # Close the signup window
        login()

    winsignup = Tk()
    winsignup.title('To Do List | Sign up')
    winsignup.geometry("500x500")

    # Heading
    heading = Label(winsignup, text='Sign up', font="Verdana 20 bold")
    heading.place(x=80, y=60)

    # username
    username_label = Label(winsignup, text='Name : ', font="Verdana 10 bold")
    username_label.place(x=80, y=100)
    username_var = StringVar()
    username_entry = Entry(winsignup, width=40, textvariable=username_var)
    username_entry.place(x=220, y=100)

    # email
    email_label = Label(winsignup, text='Email : ', font="Verdana 10 bold")
    email_label.place(x=80, y=130)
    email_var = StringVar()
    email_entry = Entry(winsignup, width=40, textvariable=email_var)
    email_entry.place(x=220, y=130)

    # Password
    password_label = Label(winsignup, text='Password :', font="Verdana 10 bold")
    password_label.place(x=80, y=160)
    password_var = StringVar()
    password_entry = Entry(winsignup, width=40, show='*', textvariable=password_var)
    password_entry.place(x=220, y=160)

    # Confirm password
    cr_password_label = Label(winsignup, text='Verify Password :', font="Verdana 10 bold")
    cr_password_label.place(x=80, y=190)
    cr_password_var = StringVar()
    cr_password_entry = Entry(winsignup, width=40, show='*', textvariable=cr_password_var)
    cr_password_entry.place(x=220, y=190)

    # Already have an account link
    login_link = Label(winsignup, text="Already have an account? Login", font="Verdana 10 underline", fg="blue", cursor="hand2")
    login_link.place(x=80, y=250)
    login_link.bind("<Button-1>", lambda e: open_login())

    # Sign up Button
    btn_signup = Button(winsignup, width=20, text='Sign up', font="Verdana 10 bold", command=action)
    btn_signup.place(x=80, y=280)

    winsignup.mainloop()


signup()
