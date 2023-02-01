usernames = []
passwords = []
names = []


def register():
    names.append(input("Enter your name:"))
    usernames.append(input("choose your username:"))
    passwords.append(input("choose your password:"))


def login():
    username = input("Enter your username:")
    password = input("Enter your Password:")
    if username in usernames and password in passwords:
        print("Welcome "+ names)
    else:
        print("Wrong username or password! Please try again.")


while True:
    account_ans = input("choose:  a)Sign Up     b)login    c)quit ")
    if account_ans == "a":
        register()
    if account_ans == "b":
        login()
    if account_ans == "c":
        break