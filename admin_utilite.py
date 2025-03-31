import sqlite3, codecs

db = sqlite3.connect("messenger.db")
cursor = db.cursor()

def add_user(name, email, password):
    print("-"*50)
    cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
    db.commit()
    print("User added")
    print("-"*50)

def delete_user(user_id):
    print("-"*50)
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    db.commit()
    print("User deleted")
    print("-"*50)

def update_user(user_id, name, email, password):
    print("-"*50)
    cursor.execute("UPDATE users SET name = ?, email = ?, password = ? WHERE id = ?", (name, email, password, user_id))
    db.commit()
    print("User updated")
    print("-"*50)

def get_users():
    print("-"*50)
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    for user in result:
        print(f"ID: {user[0]}\nName: {user[1]}\nEmail: {user[2]}\nPassword: {user[3]}")
        print(" -"*20)
    print("-"*50)

def get_messages(user_id):
    print("-"*50)
    cursor.execute("SELECT * FROM messages WHERE from_id = ? OR to_id = ?", (user_id, user_id))
    result = cursor.fetchall()
    print(" -"*20)
    for message in result:
        print(f"ID: {message[0]}\nFrom: {message[1]}\nTo: {message[2]}\nMessage: {message[3]}\nTime: {message[4]}")
        print(" -"*20)
    print("-"*50)

def delete_message(message_id):
    print("-"*50)
    cursor.execute("DELETE FROM messages WHERE id = ?", (message_id,))
    db.commit()
    print("Message deleted")
    print("-"*50)

def update_message(message_id, from_id, to_id, message):
    print("-"*50)
    cursor.execute("UPDATE messages SET from_id = ?, to_id = ?, message = ? WHERE id = ?", (from_id, to_id, message, message_id))
    db.commit()
    print("Message updated")
    print("-"*50)

def shell():
    print(r"""
               _             _              _____                     _ 
     /\       | |           (_)            |  __ \                   | |
    /  \    __| | _ __ ___   _  _ __       | |__) |__ _  _ __    ___ | |
   / /\ \  / _` || '_ ` _ \ | || '_ \      |  ___// _` || '_ \  / _ \| |
  / ____ \| (_| || | | | | || || | | |     | |   | (_| || | | ||  __/| |
 /_/    \_\\__,_||_| |_| |_||_||_| |_|     |_|    \__,_||_| |_| \___||_|
                                                                        
                                                                        """)
    print("-"*50)
    while True:
        print("1. Add user")
        print("2. Delete user")
        print("3. Update user")
        print("4. Get users")
        print("5. Get messages")
        print("6. Delete message")
        print("7. Update message")
        print("0. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            print("-"*50)
            name = input("Enter name: ")
            email = input("Enter email: ")
            password = input("Enter password: ")
            add_user(name, email, password)
        elif choice == "2":
            print("-"*50)
            user_id = input("Enter user ID: ")
            delete_user(user_id)
        elif choice == "3":
            print("-"*50)
            user_id = input("Enter user ID: ")
            name = input("Enter name: ")
            email = input("Enter email: ")
            password = input("Enter password: ")
            update_user(user_id, name, email, password)
        elif choice == "4":
            get_users()
        elif choice == "5":    
            print("-"*50)
            user_id = input("Enter user ID: ")
            get_messages(user_id)
        elif choice == "6":
            print("-"*50)
            message_id = input("Enter message ID: ")
            delete_message(message_id)
        elif choice == "7":
            print("-"*50)
            message_id = input("Enter message ID: ")
            from_id = input("Enter from ID: ")
            to_id = input("Enter to ID: ")
            message = input("Enter message: ")
            update_message(message_id, from_id, to_id, message)
        elif choice == "0":
            db.close()
            break
        else:
            print("-"*50)
            print(f"Invalid choice\n{"-"*50}")


if __name__ == "__main__":
    passwd = input("Enter password: ")
    if passwd != codecs.decode("494e56414c494420424c594154205455504f49", "hex").decode("utf-8"):
        print("Invalid password")
        input("Press enter to exit")
    else: shell()