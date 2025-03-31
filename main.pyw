import sqlite3, tkinter, tkinter.messagebox, sys, time
from tkinter import ttk

db = sqlite3.connect("messenger.db", uri=True)
cursor = db.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_id INTEGER NOT NULL,
        to_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        time_send DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")

db.commit()


def update():
    pass # UPDATE users SET <poles> = '3' WHERE id = 12345

def logout():
    global logged, id_user, username
    if not logged:
        tkinter.messagebox.showerror("Error", "You are not logged in!")
    else:
        logged = False
        username = ""
        id_user = 0
        username_text.config(text=f"Login or register")

def register():
    wnd_register = tkinter.Tk()
    wnd_register.config(bg="#020270")
    wnd_register.title("Register")
    wnd_register.geometry("400x200")
    wnd_register.resizable(False, False)
    
    name_text = tkinter.Label(wnd_register, text="Name", font=("Courier", 14, "bold"), bg="#020270", fg="#FFFFFF")
    name_text.place(x = 20, y = 10)
    
    name_entry = tkinter.Entry(wnd_register, font=("Courier", 14, "bold"), bg="#fff", fg="#000")
    name_entry.place(x = 160, y = 10)
    
    email_text = tkinter.Label(wnd_register, text="Email", font=("Courier", 14, "bold"), bg="#020270", fg="#FFFFFF")
    email_text.place(x = 20, y = 60)
    
    email_entry = tkinter.Entry(wnd_register, font=("Courier", 14, "bold"), bg="#fff", fg="#000")
    email_entry.place(x = 160, y = 60)
    
    password_text = tkinter.Label(wnd_register, text="Password", font=("Courier", 14, "bold"), bg="#020270", fg="#FFFFFF")
    password_text.place(x = 20, y = 110)
    
    password_entry = tkinter.Entry(wnd_register, font=("Courier", 14, "bold"), bg="#fff", fg="#000")
    password_entry.place(x = 160, y = 110)
    
    def register():
        name_get = name_entry.get()
        email_get = email_entry.get()
        if not name_get or not email_get or not password_entry.get(): tkinter.messagebox.showerror("Error", "All fields must be filled!"); wnd_register.focus_set(); return
        if "@" not in email_get or "." not in email_get: tkinter.messagebox.showerror("Error", "Email must contain '@' and '.'"); wnd_register.focus_set(); return
        password_get = password_entry.get()
        try: cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name_get, email_get, password_get))
        except sqlite3.IntegrityError: tkinter.messagebox.showerror("Error", "User already created!"); wnd_register.focus_set()
        else:
            global username, id_user, logged, email, password
            id_user = cursor.lastrowid
            cursor.execute("SELECT * FROM users WHERE id = ?", (id_user,))
            result = cursor.fetchone()
            username = result[1]
            email = result[2]
            password = result[3]
            logged = True
            db.commit()
            wnd_register.destroy()
            username_text.config(text=f"Hello, {username}")
            username_entry.config(state=tkinter.NORMAL)
            message_entry.config(state=tkinter.NORMAL)
            send_btn.config(state=tkinter.NORMAL)
            contacts_list.config(state=tkinter.NORMAL)
            save_contact_btn.config(state=tkinter.NORMAL)
    
    register_btn = tkinter.Button(wnd_register, text="Register", font=("Courier", 14, "bold"), bg="#202099", fg="#FFFFFF", activebackground="#2020c8", activeforeground="#FFFFFF", command=register)
    register_btn.place(height = 40, width = 160, x = 100, y = 150)
    
    wnd_register.mainloop()
def login():
    wnd_login = tkinter.Tk()
    wnd_login.config(bg="#020270")
    wnd_login.title("Login")
    wnd_login.geometry("400x200")
    wnd_login.resizable(False, False)
    
    email_text = tkinter.Label(wnd_login, text="Username", font=("Courier", 14, "bold"), bg="#020270", fg="#FFFFFF")
    email_text.place(x = 20, y = 50)
    
    email_entry = tkinter.Entry(wnd_login, font=("Courier", 14, "bold"), bg="#fff", fg="#000")
    email_entry.place(x = 160, y = 50)
    
    password_text = tkinter.Label(wnd_login, text="Password", font=("Courier", 14, "bold"), bg="#020270", fg="#FFFFFF")
    password_text.place(x = 20, y = 100)
    
    password_entry = tkinter.Entry(wnd_login, font=("Courier", 14, "bold"), bg="#fff", fg="#000")
    password_entry.place(x = 160, y = 100)

    def login_main():
        global logged, id_user, username, email, password
        name_get = email_entry.get()
        password_get = password_entry.get()
        cursor.execute("SELECT * FROM users WHERE name = ? AND password = ?", (name_get, password_get))
        result = cursor.fetchone()
        if result:
            wnd_login.destroy()
            logged = True
            id_user = result[0]
            username = result[1]
            email = result[2]
            password = result[3]
            username_text.config(text=f"Hello, {username}")
            username_entry.config(state=tkinter.NORMAL)
            message_entry.config(state=tkinter.NORMAL)
            send_btn.config(state=tkinter.NORMAL)
            contacts_list.config(state=tkinter.NORMAL)
            save_contact_btn.config(state=tkinter.NORMAL)
        else:
            tkinter.messagebox.showerror("Error", "Wrong email or password!")

    login_btn = tkinter.Button(wnd_login, text="Login", font=("Courier", 14, "bold"), bg="#202099", fg="#FFFFFF", activebackground="#2020c8", activeforeground="#FFFFFF", command=login_main)
    login_btn.place(height = 40, width = 160, x = 130, y = 145)


    wnd_login.mainloop()
     # SELECT * FROM students WHERE student_id = 12345

def info():
    tkinter.messagebox.showinfo("Info", f"ID: {id_user}\nUsername: {username}\nEmail: {email}\nPassword: {password}") if logged else tkinter.messagebox.showerror("Error", "You are not logged in!")

def exiting():
    sys.exit(0)
    db.commit()
    db.close()

def send_message():
    global user_setted_list
    to_user = username_entry.get()
    message = message_entry.get()
    to_id = 0
    cursor.execute("SELECT id FROM users WHERE name = ?", (to_user,))
    result = cursor.fetchone()
    if result:
        to_id = result[0]
    else:
        tkinter.messagebox.showerror("Error", "User not found!")
        return
    cursor.execute("INSERT INTO messages (from_id, to_id, message) VALUES (?, ?, ?)", (id_user, to_id, message))
    db.commit()
    username_entry.delete(0, tkinter.END)
    message_entry.delete(0, tkinter.END)
    username_entry.insert(0, user_setted_list)

def all_messages():
    if not logged:
        tkinter.messagebox.showerror("Error", "You are not logged in!")
        return
    wnd_messages = tkinter.Tk()
    wnd_messages.config(bg="#020270")
    wnd_messages.title("Messages")
    wnd_messages.geometry("400x200")
    wnd_messages.resizable(False, False)
    messages_text = tkinter.Text(wnd_messages, font=("Courier", 11, "bold"), bg="#fff", fg="#000", width=40, height=8)
    messages_text.place(x = 20, y = 20)
    scrollbar = tkinter.Scrollbar(wnd_messages, orient="vertical", command=messages_text.yview)
    scrollbar.place(x = 380, y = 20, height = 150)
    messages_text.config(yscrollcommand=scrollbar.set)
    text_inserted = ""
    cursor.execute("SELECT * FROM messages WHERE from_id = ? OR to_id = ?", (id_user, id_user))
    result = cursor.fetchall()
    print(result)
    for message in result:
        cursor.execute("SELECT name FROM users WHERE id = ?", (message[1],))
        username_1 = cursor.fetchall()
        cursor.execute("SELECT name FROM users WHERE id = ?", (message[2],))
        username_2 = cursor.fetchall()
        text_inserted += f"{username_1[0][0]} -> {username_2[0][0]}:\n{message[3]}\n[{message[4]}]\n{"-"*40}"
    messages_text.insert(tkinter.END, text_inserted)
    messages_text.config(state=tkinter.DISABLED)

    wnd_messages.mainloop()

def palka_1():
    global logged
    return logged

def get_new_message():
    if not palka_1():
        wnd.after(5000, get_new_message)
        return
    
    cursor.execute("SELECT * FROM messages WHERE to_id = ? ORDER BY id DESC LIMIT 1", (id_user,))
    last_message = cursor.fetchone()
    
    if last_message:
        cursor.execute("SELECT name FROM users WHERE id = ?", (last_message[1],))
        username = cursor.fetchall()
        new_message_text.config(text=f"New message: [{username[0]}, {last_message[4]}] {last_message[3]}")
    else:
        new_message_text.config(text="New message:\nEmpty...")
    
    wnd.after(5000, get_new_message)  # Повторить каждые 5 секунд

def set_contact(voider = ""):
    global user_setted_list
    user_setted_list = contacts_list.get()
    username_entry.delete(0, tkinter.END)
    username_entry.insert(0, user_setted_list)

def save_contact(voider = ""):
    contacts_list['values'] = tuple(list(contacts_list['values']) + [username_entry.get()])

logged = False
id_user = 0
username = ""
email = ""
password = ""
user_setted_list = ""

wnd = tkinter.Tk()
wnd.config(bg="#020270")
wnd.title("Messenger")
wnd.geometry("1200x600")
wnd.resizable(False, False)

# LABELS

main_text = tkinter.Label(wnd, text="Messenger", font=("Courier", 20, "bold"), bg="#020270", fg="#FFFFFF")
main_text.place(relx=0.5, rely=0.1, anchor="center")

username_text = tkinter.Label(wnd, text=f"Hello, {username}" if logged else "Login or register", font=("Courier", 14, "bold"), bg="#020270", fg="#FFFFFF")
username_text.place(x = 890, y = 20)

username_get_text = tkinter.Label(wnd, text="Username:", font=("Courier", 16, "bold"), bg="#020270", fg="#FFFFFF")
username_get_text.place(x = 450, y = 150)

message_get_text = tkinter.Label(wnd, text="Message:", font=("Courier", 16, "bold"), bg="#020270", fg="#FFFFFF")
message_get_text.place(x = 450, y = 180)

new_message_text = tkinter.Label(wnd, text="New message:\nEmpty...", font=("Courier", 18, "bold"), bg="#020270", fg="#FFFFFF")
new_message_text.place(x = 20, y = 500)

contacts_text = tkinter.Label(wnd, text=f"Contacts:", font=("Courier", 16, "bold"), bg="#020270", fg="#FFFFFF")
contacts_text.place(x = 920, y = 100)

# BUTTONS

login_btn = tkinter.Button(wnd, text="Login", font=("Courier", 14, "bold"), bg="#202099", fg="#FFFFFF", activebackground="#2020c8", activeforeground="#FFFFFF", command=login)
login_btn.place(height = 40, width = 160, x = 5, y = 20)

register_btn = tkinter.Button(wnd, text="Register", font=("Courier", 14, "bold"), bg="#202099", fg="#FFFFFF", activebackground="#2020c8", activeforeground="#FFFFFF", command=register)
register_btn.place(height = 40, width = 160, x = 5, y = 70)

logout_btn = tkinter.Button(wnd, text="Logout", font=("Courier", 14, "bold"), bg="#202099", fg="#FFFFFF", activebackground="#2020c8", activeforeground="#FFFFFF", command=logout)
logout_btn.place(height = 40, width = 160, x = 5, y = 120)

info_btn = tkinter.Button(wnd, text="Info", font=("Courier", 14, "bold"), bg="#202099", fg="#FFFFFF", activebackground="#2020c8", activeforeground="#FFFFFF", command=info)
info_btn.place(height = 40, width = 160, x = 5, y = 170)

messages_btn = tkinter.Button(wnd, text="Messages", font=("Courier", 14, "bold"), bg="#202099", fg="#FFFFFF", activebackground="#2020c8", activeforeground="#FFFFFF", command=all_messages)
messages_btn.place(height = 40, width = 160, x = 5, y = 220)

exit_btn = tkinter.Button(wnd, text="Exit", font=("Courier", 14, "bold"), bg="#202099", fg="#FFFFFF", activebackground="#2020c8", activeforeground="#FFFFFF", command=exiting)
exit_btn.place(height = 40, width = 160, x = 5, y = 270)

save_contact_btn = tkinter.Button(wnd, text="Save contact", font=("Courier", 14, "bold"), bg="#202099", fg="#FFFFFF", activebackground="#2020c8", activeforeground="#FFFFFF", command=save_contact, state=tkinter.DISABLED)
save_contact_btn.place(height = 40, width = 160, x = 640, y = 240)

send_btn = tkinter.Button(wnd, text="Send", font=("Courier", 14, "bold"), bg="#202099", fg="#FFFFFF", activebackground="#2020c8", activeforeground="#FFFFFF", command=send_message, state=tkinter.DISABLED)
send_btn.place(height = 40, width = 160, x = 450, y = 240)

# ----- ENTRIES -----

username_entry = tkinter.Entry(wnd, font=("Courier", 14, "bold"), bg="#fff", fg="#000", state=tkinter.DISABLED)
username_entry.place(x = 600, y = 150)

message_entry = tkinter.Entry(wnd, font=("Courier", 14, "bold"), bg="#fff", fg="#000", state=tkinter.DISABLED)
message_entry.place(x = 600, y = 180)

contacts_list = tkinter.ttk.Combobox(wnd, font=("Courier", 14, "bold"), values = ["ADMIN"], state=tkinter.DISABLED)
contacts_list.place(x = 870, y = 150)

wnd.protocol("WM_DELETE_WINDOW", exiting)
contacts_list.bind("<<ComboboxSelected>>", set_contact)

get_new_message()
wnd.mainloop()