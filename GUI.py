import tkinter as tk
from tkinter import messagebox

loggedIn = False

def attempt_login(username, password):
    if username == 'admin' and password == 'password':
        return True
    else:
        return False

def connected():
    root.destroy()
    root2 = tk.Tk()
    root2.title('Login to Server')
    root2.geometry('640x480+300+300')
    root2.resizable(True, True)

    title2 = tk.Label(
        root2,
        text='Welcome to the server, please log in.',
        font=('Arial', 16, 'bold'),
        fg='blue',
        width=30,
        height=2
    )
    title2.pack(pady=10)

    username = tk.StringVar()
    password = tk.StringVar()

    username_label = tk.Label(root2, text="Username:", font=('Times New Roman', 14))
    username_label.pack(pady=5)
    userinput = tk.Entry(root2, textvariable=username)
    userinput.pack(pady=5)

    password_label = tk.Label(root2, text="Password:", font=('Times New Roman', 14))
    password_label.pack(pady=5)
    passinput = tk.Entry(root2, textvariable=password, show='*')
    passinput.pack(pady=5)

    def login_action():
        user = username.get()
        passw = password.get()

        if attempt_login(user, passw):
            root2.destroy()
            logged_in_window()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password!")

    login_button = tk.Button(root2, text='Log In', fg='blue', command=login_action)
    login_button.pack(pady=20)

    root2.mainloop()

def logged_in_window():
    root3 = tk.Tk()
    root3.title('Welcome')
    root3.geometry('640x480+300+300')
    root3.resizable(True, True)

    welcome_label = tk.Label(
        root3,
        text='You are now logged in.',
        font=('Arial', 16, 'bold'),
        fg='green',
        width=30,
        height=10
    )
    welcome_label.pack()

    def upload_action():
        print("Upload Button Clicked")

    def download_action():
        print("Download Button Clicked")

    def logout_action():
        print("Logout Button Clicked")

    def show_stats_action():
        print("Show Statistics Button Clicked")

    def directories_action():
        print("Directories Button Clicked")

    def subfolders_action():
        print("Subfolder Button Clicked")

    button_frame = tk.Frame(root3)
    button_frame.pack(pady=20)

    upload_button = tk.Button(button_frame, text="Upload", fg='blue', command=upload_action)
    upload_button.pack(side='left', padx=5)

    download_button = tk.Button(button_frame, text="Download", fg='blue', command=download_action)
    download_button.pack(side='left', padx=5)

    logout_button = tk.Button(button_frame, text="Logout", fg='blue', command=logout_action)
    logout_button.pack(side='left', padx=5)

    show_stats_button = tk.Button(button_frame, text="Show Statistics", fg='blue', command=show_stats_action)
    show_stats_button.pack(side='left', padx=5)

    directories_button = tk.Button(button_frame, text="Directories", fg='blue', command=directories_action)
    directories_button.pack(side='left', padx=5)

    subfolders_button = tk.Button(button_frame, text="Subfolder", fg='blue', command=subfolders_action)
    subfolders_button.pack(side='left', padx=5)

    root3.mainloop()

root = tk.Tk()
root.title('File Server')
root.geometry('640x480+300+300')
root.resizable(True, True)

title = tk.Label(
    root,
    text='Connect to the server',
    font=('Arial', 16, 'bold'),
    fg='blue',
    width=30,
    height=10
)
title.pack()

connect_button = tk.Button(root, text='Connect', fg='blue', command=connected)
connect_button.pack(pady=20)

root.mainloop()
