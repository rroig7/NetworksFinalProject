import tkinter as tk
from tkinter.ttk import Button


#def try_to_connect():
    



def connected():

    root.destroy()

    # Create and display the second window (root2)
    root2 = tk.Tk()
    root2.title('Welcome')
    root2.geometry('640x480+300+300')
    root2.resizable(True, True)


    title2 = tk.Label(
        root2,
        text='Welcome to the server, please log in.',
        font=('Arial', 16, 'bold'),
        fg='blue',
        width=30,
        height=10
    )
    title2.pack()
    username = tk.StringVar(root2)
    password = tk.StringVar(root2)
    username_label = tk.Label(root2, text="Username:", font=('Times New Roman', 14))
    username_label.pack(pady=5)
    userinput = tk.Entry(root2, textvariable=username)
    userinput.pack(pady=5)
    password_label = tk.Label(root2, text="Password:", font=('Times New Roman', 14))
    password_label.pack(pady=5)
    passinput = tk.Entry(root2, textvariable=password)
    passinput.pack(pady=5)
    button = tk.Button(root2, text='Log in', fg='blue')
    button.pack()
    root2.mainloop()




root = tk.Tk()
root.title('File server')
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


button = tk.Button(root, text='Connect', fg='blue', command=connected)
button.pack()


root.mainloop()
